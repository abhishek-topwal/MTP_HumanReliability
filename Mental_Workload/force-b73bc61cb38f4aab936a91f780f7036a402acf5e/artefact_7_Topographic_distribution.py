import numpy as np

""" 4).7 Topographic distribution of standard deviations """
def Topographic_distribution(ICs_projections, info):
    pre_frontal_chanels = []
    pre_other_chanels = []
    marked_ICs = np.zeros(64)
    for i in range(np.size(info['ch_names'])):
        if ((info['ch_names'][i].find('F') != -1) or ((info['ch_names'][i].find('f') != -1))):
            pre_frontal_chanels.append(i)
        else:
            pre_other_chanels.append(i)
    frontal_chanels = np.array(pre_frontal_chanels)
    other_chanels = np.array(pre_other_chanels)

    pre_R = []
    for i in range(np.size(ICs_projections, 2)):
        actual_projection = np.transpose(ICs_projections[:, :, i])
        actual_std_front = np.std(actual_projection[frontal_chanels, :])
        actual_std_other = np.std(actual_projection[other_chanels, :])
        actual_R = actual_std_front / actual_std_other
        pre_R.append(actual_R)

    R = np.array(pre_R)
    mean_R = np.mean(R)
    std_R = np.std(R)
    for i in range(np.size(R, 0)):
        if (R[i] > (mean_R + std_R)):
            marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs