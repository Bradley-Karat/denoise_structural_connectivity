import numpy as np
import random
import bipca
from bipca import plotting
from bipca import utils

def denoise_matrix(X, threshold=10):

    '''
    X: array (M, M, N)
        Input streamline count matrix, where M is number of regions and N is number of subjects
    Threshold: int
        Global nonzero threshold for the rows and columns of the matrix (default=10)

    Returns:
    X_d: array (M, M, N)
        Denoised streamline count matrix, where M is number of regions and N is number of subjects
    KS_mean: scalar
        Mean Kolmogorov-Smirnov statistic for how closely the denoised spectrum follows the MP distribution. 
    spectrum: list
        Returns the plotting spectrum of variable size depending on the number of submatrices empirically chosen for denoising
    '''

    N = X.shape[-1]
    M = X.shape[0]

    # Extract only lower triangle for each subject
    conn_extract = np.zeros((N,len(np.tril_indices(M,k=-1)[0])))

    for ii in range(N):
        conn_extract[ii,:] = X[:,:,ii][np.tril_indices(M,k=-1)]

    # Threshold extracted connectivity matrix
    conn_stabilized,indices_used = utils.stabilize_matrix(conn_extract,threshold=threshold)    

    # Pragmatic estimate of bin size
    if (conn_stabilized.shape[1] / conn_stabilized.shape[0]) > 1:
        bin_divisor = int(np.round((conn_stabilized.shape[1] / conn_stabilized.shape[0]) / 2))
        bin_size = int(np.round(conn_stabilized.shape[1] / bin_divisor))
    else:
        bin_divisor = 1
        bin_size = int(np.round(conn_stabilized.shape[1] / bin_divisor))

    X_d_filt = np.zeros((conn_stabilized.shape))
    spectrum = []
    KS_hold = np.empty((bin_divisor))

    start_ind = 0
    end_ind = 0
    ind_hold = random.sample(range(0, conn_stabilized.shape[1]), conn_stabilized.shape[1])

    for ii in range(bin_divisor):

        op = bipca.BiPCA(n_components=-1) # get the BiPCA operator, here n_components=-1 is to do full SVD

        start_ind = ii * bin_size # extracting sub-matrix to denoise from full connectivity matrix
        end_ind = start_ind + bin_size

        ind_bin = ind_hold[start_ind:end_ind]

        X_d_filt[:,ind_bin] = op.fit_transform(conn_stabilized[:,ind_bin]) # take the count data as input and run bipca

        op.get_plotting_spectrum(get_raw=True) # get the fitting parameters
        spectrum.append(op) # get the fitting parameters
        KS_hold[ii] = op.best_kst[0]


    X_d_full = np.zeros((N,len(np.tril_indices(M,k=-1)[0])))

    # Place denoised counts back into pre-filtered matrix size
    X_d_full[np.reshape(indices_used[0],(N,1)),np.reshape(indices_used[1],(1,conn_stabilized.shape[1]))] = X_d_filt 

    # Reshape back to original input matrix size
    X_d = np.zeros((M,M,N))
    lower_ind = np.tril_indices(M,k=-1)
    X_d[lower_ind[0],lower_ind[1],:] = X_d_full.T
    
    for i in range(N):
        X_d[:,:,i] = X_d[:,:,i] + X_d[:,:,i].T


    return X_d, np.mean(KS_hold), spectrum
