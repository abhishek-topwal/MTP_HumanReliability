import numpy as np
import pywt
import concurrent.futures
import matplotlib.pyplot as plt
import mne
from mne.io import read_raw_edf


from artefact_1_AMI import *
from artefact_2_Spiking import *
from artefact_3_Kurtosis import *
from artefact_4_5_PSD import *
from artefact_6_Projection_STD import *
from artefact_7_Topographic_distribution import *
from artefact_8_Amplitude_thresholding import *
from artefact_Spike_zone_thresholding import *

# from preprocess.artefact_1_AMI import *
# from preprocess.artefact_2_Spiking import *
# from preprocess.artefact_3_Kurtosis import *
# from preprocess.artefact_4_5_PSD import *
# from preprocess.artefact_6_Projection_STD import *
# from preprocess.artefact_7_Topographic_distribution import *
# from preprocess.artefact_8_Amplitude_thresholding import *
# # from preprocess.artefact_Spike_zone_thresholding import *
# from preprocess.artefact_PSD import *
from sklearn.decomposition import FastICA

""" This implementation is based on FORCe: Fully Online and Automated Artifact
Removal for Brain-Computer Interfacing by Ian Daly, Reinhold Scherer, Martin Billinger, and Gernot Müller-Putz."""

""" Constants: """
# 4.1 AMI
LAG_OFFSET = 60
THRESHOLD_MAX = 2.0
THRESHOLD_MIN = 1.0
# 4.2 Spiking
THRESHOLD_COEFF = 0.25
# 4.4-5 PSD + Gamma
DISTANCE = 3.5
THRESHOLD_GAMMA = 1.7
# 4.8 Large amplitude removing
THRESHOLD_AMPLITUDE = 100
PEAK_DIFFERENCE = 60
# 5 Spike-zone thresholding
DC_checkVal = 0.2
DC_adjustVal = 0.07
AC_checkVal = 0.7
AC_adjustVal = 0.8

REMOVING_THRESHOLD = 3


def FORCe(info, original_data):
    nCh = len(info['chs'])
    data = np.multiply(original_data, 1e6)

    """ Step 1) - 4) """
    waveletname = 'sym4'
    coeffitiantsLevel1 = []
    coeffitiantsLevel2 = []
    cA2 = []
    cD1 = []
    cD2 = []
    marked_ICs = np.zeros(nCh)

    """
    # ''cAx'' is he array of approximation coefficient (low pass filters) and
    # ''cDx'' is the list of detail coefficients (high pass filters).
    # 2 level decomposition!
    """

    for i in range(np.size(data, 0)):
        actual_coeff = pywt.wavedec(data[i][:], waveletname, level=1)
        cA1_actual, cD1_actual = actual_coeff
        coeffitiantsLevel1.append(actual_coeff)
        cD1.append(cD1_actual)
    D1 = np.array(cD1)

    for i in range(np.size(data, 0)):
        actual_coeff = pywt.wavedec(data[i][:], waveletname, level=2)
        cA2_actual, cD2_actual, cD1_actual = actual_coeff
        coeffitiantsLevel2.append(actual_coeff)
        cA2.append(cA2_actual)
        cD2.append(cD2_actual)
    A2 = np.array(cA2)
    D2 = np.array(cD2)

    """
    # S: 2D array containing estimated source signals
    # A: 2D array containing mixing matrix, i.e. A.dot(S) = X
    """
    ica = FastICA(n_components=len(info['chs']), algorithm='parallel',max_iter=500,tol=1e-2)
    S = ica.fit(A2.T).transform(A2.T)
    A = ica.mixing_
    assert np.allclose(A2.T, np.dot(S, A.T) + ica.mean_)
    assert A.shape[0] == A.shape[1]

    ICs_projections = np.zeros((np.size(S, 0), np.size(S, 1), np.size(S, 1)))
    for i in range(np.size(S, 1)):
        actual_S = np.copy(S)
        for j in range(np.size(S, 1)):
            if (j != i):
                actual_S[:, j] = 0
        actual_projection = np.dot(actual_S, A.T)
        ICs_projections[:, :, i] = actual_projection

    with concurrent.futures.ThreadPoolExecutor() as executor:
        toRemoveICs1 = executor.submit(Auto_Mutual_Information, ICs_projections, LAG_OFFSET, THRESHOLD_MAX, THRESHOLD_MIN)
        toRemoveICs2 = executor.submit(Spiking_activity, S, THRESHOLD_COEFF)
        toRemoveICs3 = executor.submit(Kurtosis, ICs_projections)
        toRemoveICs4 = executor.submit(PSD, ICs_projections, info['sfreq'], DISTANCE, THRESHOLD_GAMMA)
        toRemoveICs5 = executor.submit(Projection_STD, ICs_projections)
        toRemoveICs6 = executor.submit(Topographic_distribution, ICs_projections, info)
        toRemoveICs7 = executor.submit(Amplitude_thresholding, ICs_projections, THRESHOLD_AMPLITUDE, PEAK_DIFFERENCE)

    for i in range(np.size(marked_ICs)):
         marked_ICs[i] = toRemoveICs1.result()[i] + toRemoveICs2.result()[i] + toRemoveICs3.result()[i] + toRemoveICs4.result()[i] + toRemoveICs5.result()[i] + toRemoveICs6.result()[i] + toRemoveICs7.result()[i]

    # Without paralellisation:
    """ Step 4).1: Auto-Mutal Informatin """
    # toRemoveICs1 = Auto_Mutual_Information(ICs_projections, LAG_OFFSET, THRESHOLD_MAX, THRESHOLD_MIN, marked_ICs)
    # print('Marked to remove by AMI: ', toRemoveICs1)

    """ Step 4).2: Spiking activity """
    # toRemoveICs2a, toRemoveICs2b = Spiking_activity(S, THRESHOLD_COEFF, marked_ICs)
    # print('Marked to remove by Spiking-activity: ', toRemoveICs2a)
    # print('Marked to remove by Spike zone coefficients: ', toRemoveICs2b)

    """ 4).3 Kurtosis """
    # toRemoveICs3 = Kurtosis(ICs_projections, marked_ICs)
    # print('Marked to remove by Kurtosis : ', toRemoveICs3)    # data = raw_croped.get_data(picks = chanls)

    # toRemoveICs4, toRemoveICs5 = PSD(ICs_projections, info['sfreq'], DISTANCE, THRESHOLD_GAMMA, marked_ICs)
    # print('Marked to remove by PSD & 1/F distribution: ', toRemoveICs4)
    # print('Marked to remove by Gamma frequency: ', toRemoveICs5)

    """ 4).6 Check stds of projections of ICs. """
    # toRemoveICs6 = Projection_STD(ICs_projections, marked_ICs)
    # print('Marked to remove by Std: ', toRemoveICs6)

    """ 4).7 Topographic distribution of standard deviations """
    # toRemoveICs7 = Topographic_distribution(ICs_projections, info, marked_ICs)
    # print('Marked to remove by topographic distribution: ', toRemoveICs7)

    """ 4).8 Remove ICs with large amplitudes """
    # toRemoveICs8a, toRemoveICs8b = Amplitude_thresholding(ICs_projections, THRESHOLD_AMPLITUDE, PEAK_DIFFERENCE,
    #                                                       marked_ICs)
    # print('Marked to remove by Large amplitudes A: ', toRemoveICs8a)
    # print('Marked to remove by Large amplitudes B: ', toRemoveICs8b)

    for i in range(np.size(marked_ICs)):
        if (marked_ICs[i] > REMOVING_THRESHOLD):
            S[:, i] = 0

    clean_A2 = (ica.inverse_transform(S)).T

    """ 5) Spike Zone Thresholding """
    newD1 = Thresholding(D1, DC_checkVal, DC_adjustVal)
    newA2 = Thresholding(clean_A2, AC_checkVal, AC_adjustVal)
    newD2 = Thresholding(D2, DC_checkVal, DC_adjustVal)

    print("Number of channel markings: ", marked_ICs)

    pre_clea_data = []
    for i in range(np.size(D2, 0)):
        coeff = [newA2[i], newD2[i], newD1[i]]
        actual_reconstuction = pywt.waverec(coeff, waveletname)
        pre_clea_data.append(actual_reconstuction)

    clean_data = np.array(pre_clea_data)
    return clean_data

class ArtefactFilter:

    def offline_filter(self, epochs):
        """Offline Faster algorithm

        Filters the input epochs, and saves the parameters (such as ICA weights),
        for the possibility of online filtering

        Parameters
        ----------
        epochs : mne.Epochs
            The epochs to analyze

        Returns
        -------
        mne.Epochs
            The filtered epoch
        """
        for i in range(len(epochs)):
            epochs._data[i, ...] = FORCe(epochs.info, epochs[i].get_data()[0])[:,:-1]
        return epochs


if __name__ == '__main__':

    # file_name = 'F:/ÖNLAB/Databases/physionet.org/physiobank/database/eegmmidb/S001/S001R03.edf'
    file_name = '/home/abhishek/Documents/MTP_HumanReliability/Mental_Workload/Cognitive-Mental-workload-Classification/Training-Data/S01/1-Back/S01-01-25.09.2016.10.21.24.edf'
    original_raw = read_raw_edf(file_name)
    raw = original_raw.copy()
    raw.pick_channels(['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'])

    chanls = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    raw_croped = raw.crop(tmax=60).load_data()
    raw_croped.resample(500)
    data = raw_croped.get_data()

    # Added a band pass filter of range 1-40 Hz
    mne.filter.filter_data(data,sfreq=128,l_freq=1,h_freq=40)


    sampling_freq = raw.info['sfreq']
    chanel_number = np.size(raw.info['ch_names'])

    """ The following parameters must always be set manually! """
    windowLengthCoeff = 1
    windowLength = int(windowLengthCoeff * sampling_freq)
    # Whole data length:
    N = windowLength * (int(np.size(data, 1) / windowLength))
    # Just for a partition of data:
    # N = windowLength * 10
    rest = np.size(data, 1) - N
    preEEG_clean = []

    for windowPosition in range(0, N, windowLength):
        window = np.arange(windowPosition, (windowPosition + windowLength), 1, dtype=int)
        preEEG_clean.append(FORCe(raw_croped.info, data[:, window]))
        print('--- ' + str(window[0]) + '-' + str(window[-1]) + ' ---')

    EEG_clean = np.concatenate(preEEG_clean, axis=1)

    plt.plot(EEG_clean[0, :])
    plt.show()
    """ -- Plot all of chanels -- """
    # for i in range(np.size(EEG_clean, 0)):
    #     plt.subplot(np.size(EEG_clean, 0), 1, i+1)
    #     plt.plot(EEG_clean[i, :])
    # plt.show()

    """ -- Plot chanels grouped 8 chanels -- """
    # for i in range(int(np.size(EEG_clean, 0)/8)):
    #     for j in range(8):
    #         plt.subplot(np.size(EEG_clean, 0)/8, 1, j+1)
    #         plt.plot(np.multiply(data[(i*8)+j, :], 1e6), 'r')
    #         plt.plot(EEG_clean[(i * 8)+j, :])
    #     plt.show()

    # """ -- Plot chanels grouped 16 chanels -- """
    # for i in range(int(np.size(data, 0) / 16)):
    #     for j in range(16):
    #         plt.subplot(np.size(EEG_clean, 0) / 4, 1, j + 1)
    #         plt.plot(np.multiply(data[(i * 16) + j, :], 1e6), 'r')
    #         plt.plot(EEG_clean[(i * 16) + j, :])
    #         plt.ylabel(raw.info['ch_names'][(i * 16)+j])
    #     plt.show()