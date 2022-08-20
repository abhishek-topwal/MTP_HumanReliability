import numpy as np
import math
from scipy.fft import fft, ifft

def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]

def nextpow2(x):
    """ Function for finding the next power of 2 """
    return 1 if x == 0 else math.ceil(math.log2(x))

def powerspectrum(data, Fs):
    T = 1 / Fs
    L = np.size(data, 0)
    NFFT = 2 ** nextpow2(L)
    Y = fft(data, NFFT) / L
    f = Fs / 2 * np.linspace(0, 1, int(NFFT / 2))
    power = 2 * np.abs(Y[0:int(NFFT / 2)])
    return f, power

""" 4).4-5 Check PSDs + PSD of gamma frequency """
def PSD(ICs_projections, FS, distance, thGamma):
    gammaPSDT = []
    diff = []
    marked_ICs = np.zeros(64)
    for i in range(np.size(ICs_projections, 2)):
        if (marked_ICs[i] <= 3):
            actual_projection = np.transpose(ICs_projections[:, :, i])
            pre_diff = []
            pre_gamma = []
            for k in range(np.size(actual_projection, 0)):
                f, power = powerspectrum(actual_projection[k, :], FS)
                actual_idealDistro1 = f[1:]
                actual_idealDistro2 = np.divide(1, f[1:])

                normedActual_idealDistro2 = np.divide(actual_idealDistro2, np.max(actual_idealDistro2))
                normedPsCheck = np.divide(power[1:], np.max(power[1:]))

                actual_diff = normedPsCheck - normedActual_idealDistro2

                actual_specDistT = np.mean(math.sqrt(np.dot(actual_diff, actual_diff.T)))
                pre_diff.append(actual_specDistT)
                actual_gammaPSDT = np.mean(power[f > 30])
                pre_gamma.append(actual_gammaPSDT)

            diff.append(np.mean(np.array(pre_diff)))
            gammaPSDT.append(np.mean(np.array(pre_gamma)))
        else:
            diff.append(-1)
            gammaPSDT.append(-1)
    gammaIC = np.array(gammaPSDT)
    diffIC = np.array(diff)

    for i in range(np.size(ICs_projections, 2)):
        if (diffIC[i] > distance):
            marked_ICs[i] = marked_ICs[i] + 1
        if (gammaIC[i] > thGamma):
            marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs