import numpy as np
from numpy import ndarray, diag
from scipy.sparse import csr_array, spmatrix, triu as sptriu, tril as sptril
from typing import Union


def spdiag(data: Union[ndarray, spmatrix]) -> Union[ndarray, spmatrix]:
    """
    Sparse edquivelent of numpy function np.diag. If data is 1D ndarray, return sparse
    matrix with this along the diagonal. If data is a spmatrix, return the diagonal as
    an ndarray

    Parameters
    ----------
    data            ndarray or spamtrix

    Returns
    -------
    diag            diagonal spmatrix or diagonal of spmatrix
    """

    if isinstance(data, ndarray):
        if data.ndim != 1:
            raise ValueError('data should be a 1D numpy array')
        N = len(data)
        return csr_array((data, (np.arange(N), np.arange(N))), shape=(N, N))

    elif isinstance(data, spmatrix):
        return data.diagonal()

    else:
        raise ValueError('data should be ndarray or spmatrix')


def tensor_product(X: ndarray, *As):
    """
    Compute the product Ten((A1 ⊗ A2 ⊗ ... ⊗ AN) vec(X))

    e.g:

    X = randn(2, 3, 4)
    A1 = randn(4, 4); A2 = randn(3, 3); A3 = randn(2, 2)
    X_ = tensor_product(X, A1, A2, A3)
    """

    assert X.ndim == len(As), f'Input was expected to be {len(As)}-dimensional, but it was {X.ndim}-dimensional'
    assert all(A.shape == (s, s) for A, s in zip(As, reversed(X.shape))), f'Input was expected to have shape {tuple(A.shape[0] for A in As[::-1])} but it has shape {X.shape}'

    ans = X

    for i, A in enumerate(reversed(As)):
        ans = np.tensordot(A, ans, axes=[[1], [i]])

    return ans.transpose()



def tensor_product_of_sum(X: ndarray, *As):
    """
    Compute the product Ten((A1 ⊕ A2 ⊕ ... ⊕ AN) vec(X))

    e.g:

    X = randn(2, 3, 4)
    A1 = randn(4, 4); A2 = randn(3, 3); A3 = randn(2, 2)
    X_ = tensor_product_of_sum(X, A1, A2, A3)
    """

    assert X.ndim == len(As), f'Input was expected to be {len(As)}-dimensional, but it was {X.ndim}-dimensional'
    assert all(A.shape == (s, s) for A, s in zip(As, reversed(X.shape))), f'Input was expected to have shape {tuple(A.shape[0] for A in As[::-1])} but it has shape {X.shape}'

    ans = np.zeros_like(X)

    for i, A in enumerate(reversed(As)):
        trans = list(range(1, len(As)))
        trans.insert(i, 0)
        ans += np.tensordot(A, X, axes=[[1], [i]]).transpose(trans)

    return ans


def vec(X: ndarray) -> ndarray:
    """
    Convert a tensor of any shape into a vector
    """
    return X.reshape(-1, order='F')


def mat(x: ndarray, shape: tuple=None, like: ndarray=None) -> ndarray:
    """
    Convert a vector x into a tensor of a given shape
    """

    if x.ndim != 1:
        raise ValueError('x should be 1-dimensional')

    if shape is None and like is None:
        raise ValueError('Pass either shape or like')

    if shape is not None and like is not None:
        raise ValueError('Pass only one of shape or like')

    if shape is not None:
        return x.reshape(shape, order='F')

    elif like is not None:
        return x.reshape(like.shape, order='F')



def is_diag(A: ndarray) -> bool:
    """
    Determine whether a square array is diagonal
    """

    m, n = A.shape
    assert A.ndim == 2, 'A should be 2-dimensional'
    assert m == n, f'A should be square but it has shape {(m, n)}'
    p, q = A.strides
    return not np.any(np.lib.stride_tricks.as_strided(A[:, 1:], (m - 1, m), (p + q, q)))