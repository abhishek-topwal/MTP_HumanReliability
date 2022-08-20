import numpy as np
from scipy.stats import kurtosis

""" 4).3 Kurtosis """
def Kurtosis(ICs_projections):
    pre_IC_kurtosis = []
    marked_ICs = np.zeros(64)
    for i in range(np.size(ICs_projections, 2)):
        actual_projection = np.transpose(ICs_projections[:, :, i])
        pre_kurtosis = []
        for k in range(np.size(actual_projection, 0)):
            actual_kurtosis = kurtosis(actual_projection[k, :])
            pre_kurtosis.append(actual_kurtosis)
        pre_IC_kurtosis.append(np.mean(np.array(pre_kurtosis)))
    IC_kurtosis = np.array(pre_IC_kurtosis)

    mu = np.mean(IC_kurtosis)
    sigma = np.std(IC_kurtosis)
    for i in range(np.size(IC_kurtosis)):
        k = IC_kurtosis[i]
        if k > (mu + (0.5 * sigma)):
            marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs