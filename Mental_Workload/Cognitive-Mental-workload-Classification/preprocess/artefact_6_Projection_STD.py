import numpy as np

""" 4).6 Check stds of projections of ICs. """
def Projection_STD(ICs_projections):
    pre_thetaProjection = []
    marked_ICs = np.zeros(64)
    for i in range(np.size(ICs_projections, 2)):
        actual_projection = np.transpose(ICs_projections[:,:, i])
        pre_stds = []
        for k in range(np.size(actual_projection, 0)):
            actual_stds = np.std(actual_projection[k])
            pre_stds.append(actual_stds)
        stds = np.array(pre_stds)
        pre_thetaProjection.append(np.mean(stds))
    thetaProjection = np.array(pre_thetaProjection)

    mean_theta = np.mean(thetaProjection)
    sigma_theta = np.std(thetaProjection)

    for i in range(np.size(ICs_projections, 2)):
        if (thetaProjection[i] > (mean_theta + (2 * sigma_theta))):
            marked_ICs[i] = marked_ICs[i] + 1

    return marked_ICs