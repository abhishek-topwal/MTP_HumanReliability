import numpy as np

def Amplitude_thresholding(ICs_projections, thAmplitude, peakDifference):
    marked_ICs = np.zeros(64)

    for i in range(np.size(ICs_projections, 2)):
        if (marked_ICs[i] <= 3):
            actual_projection = np.transpose(ICs_projections[:, :, i])
            actual_mean = np.mean(actual_projection, 0)
            max_value = np.max(actual_mean)
            min_value = np.min(actual_mean)
            diff = max_value - min_value
            if (max_value > thAmplitude or min_value < -(thAmplitude)):
                marked_ICs[i] = marked_ICs[i] + 1
            if (diff > peakDifference):
                marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs