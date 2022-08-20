import numpy as np

""" 5) Spike Zone Thresholding """
def Thresholding(Coefficient, checkVal, adjustVal):
    pre_spike_Co = []
    pre_spike_position = []
    newCoeff = np.copy(Coefficient)
    for i in range(np.size(newCoeff, 0)):
        # actual_signal = abs(np.mean(Coefficient[i]))
        actual_signal = newCoeff[i]
        pre_actual_spike_position = []
        pre_actual_Co = []
        for j in range(1, np.size(actual_signal) - 1):
            if (actual_signal[j] > actual_signal[j - 1] and actual_signal[j] > actual_signal[j + 1]):
                pre_actual_spike_position.append(j)
                # Pythonban [x:y] = [x,y) => mivel az utolsó index nincs benne, j-1:j+2!
                actual_mean = np.mean(actual_signal[j - 1:j + 2])  # Itt lehet actual signal helyet ICsPrijection kell, illetve az abs-men összefüggés is zavaros.
                actual_std = np.std(actual_signal[j - 1:j + 2])
                pre_actual_Co.append(actual_mean / actual_std)
        actual_Co = np.array(pre_actual_Co)
        pre_spike_Co.append(pre_actual_Co)
        pre_spike_position.append(pre_actual_spike_position)

        threshold = adjustVal * (np.mean(actual_Co) + np.std(actual_Co))
        for k in range(np.size(pre_actual_spike_position)):
            if (pre_actual_Co[k] > threshold):
                idx = pre_actual_spike_position[k]
                newCoeff[i, idx] = checkVal * newCoeff[i, idx]

    return newCoeff