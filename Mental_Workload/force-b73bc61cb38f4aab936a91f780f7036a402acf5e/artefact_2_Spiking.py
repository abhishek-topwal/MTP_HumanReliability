import numpy as np
from scipy.signal import find_peaks

""" Step 4).2: Spiking activity """
def Spiking_activity(S,  coefficientThreshold):
    pre_spike_threshold = []
    marked_ICs = np.zeros(64)
    IC = S.T
    for i in range(np.size(IC, 0)):
        peaks_actual, _ = find_peaks(np.abs(IC[i, :]))
        actual_peak_value = np.abs(IC[i, peaks_actual])
        mean_actual = np.mean(actual_peak_value)
        std_actual = np.std(actual_peak_value)
        threshold_actual = mean_actual + (3 * std_actual)
        pre_spike_threshold.append(threshold_actual)

        if np.max(actual_peak_value) > threshold_actual:
            marked_ICs[i] = marked_ICs[i] + 1

        """ -- Spike zone coefficients -- """
        actual_signal = np.abs(IC[i])
        pre_actual_spike_position = []
        pre_actual_Co = []
        for j in range(1, np.size(actual_signal) - 1):
            if (actual_signal[j] > actual_signal[j - 1] and actual_signal[j] > actual_signal[j + 1]):
                pre_actual_spike_position.append(j)
                # Pythonban [x:y] = [x,y) => mivel az utolsó index nincs benne, j-1:j+2!
                actual_mean = np.mean(actual_signal[j - 1:j + 2])
                actual_std = np.std(actual_signal[j - 1:j + 2])
                pre_actual_Co.append(actual_mean / actual_std)
        actual_Co = np.array(pre_actual_Co)
        actual_spike_position = np.array(pre_actual_spike_position)
        threshold = 0.1 * (np.mean(actual_Co) + np.std(actual_Co))

        if (np.size(actual_Co) > 0):
            high_Co_counter = 0
            for k in range(np.size(actual_spike_position)):
                if (actual_Co[k] > threshold):
                    high_Co_counter += 1
            no_spikes = np.size(high_Co_counter) / np.size(actual_spike_position)
        else:
            no_spikes = 0

        if (no_spikes > coefficientThreshold):
            marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs