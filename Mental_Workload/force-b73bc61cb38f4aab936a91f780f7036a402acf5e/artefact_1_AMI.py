import numpy as np
import math

def calc_MI(X,Y,bins):
   c_XY = np.histogram2d(X,Y,bins)[0]
   c_X = np.histogram(X,bins)[0]
   c_Y = np.histogram(Y,bins)[0]

   H_X = shan_entropy(c_X)
   H_Y = shan_entropy(c_Y)
   H_XY = shan_entropy(c_XY)

   MI = H_X + H_Y - H_XY
   return MI

def shan_entropy(c):
    c_normalized = c / float(np.sum(c))
    c_normalized = c_normalized[np.nonzero(c_normalized)]
    H = -sum(c_normalized* np.log2(c_normalized))
    return H

""" Step 4).1: Auto-Mutal Informatin """
def Auto_Mutual_Information(ICs_projections, lag_offset, max_value, min_value):
    marked_ICs = np.zeros(64)
    pre_AMIs = []
    for i in range(np.size(ICs_projections, 2)):
        actual_projection = np.transpose(ICs_projections[:, :, i])
        lag_offsets = np.array([lag_offset])
        cAMIs = []
        for lagNo in range(np.size(lag_offsets)):
            lags = np.arange(0, math.floor(np.size(ICs_projections, 1) / 2), lag_offsets[lagNo])
            end_p = np.size(ICs_projections, 1)
            for chNo in range(np.size(actual_projection, 0)):
                actual_AMIs = []
                for k in range(np.size(lags)):
                    actual_AMIs.append(
                        calc_MI(actual_projection[chNo, 0:end_p - lags[k]], actual_projection[chNo, lags[k]:end_p], 5))
                cAMIs.append(np.mean(actual_AMIs))
        pre_AMIs.append(np.max(cAMIs))
    AMIs = np.array(pre_AMIs)

    thresholdMax = max_value
    thresholddMin = min_value

    for i in range(np.size(AMIs)):
        if (AMIs[i] > thresholdMax or AMIs[i] < thresholddMin):
            marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs