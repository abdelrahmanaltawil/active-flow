# env imports 
import numpy as np


# local imports
import active_flow.simulation.algorithm_tasks as tasks

def test_discretize() -> None:
    '''
    Placeholder
    '''
    
    L = np.pi
    N = 128

    x_vectors, dx, k_vectors, dk = tasks.discretize(
        L= L,
        N= N
    )

    # check dimensionality
    assert x_vectors[:,:,0].shape == x_vectors[:,:,1].shape == (N,N)
    assert k_vectors[:,:,0].shape == k_vectors[:,:,1].shape == (N,N)

    # factor
    assert dx == L/N
    assert dk == 2


def test_set_initial_conditions() -> None:
    '''
    Placeholder
    '''

    N = 128
    initial_w_k = tasks.set_initial_conditions(
        N= N
    )
    
    # complex items
    assert initial_w_k.dtype == np.complex128
    
    # preserve shape
    assert initial_w_k.shape == (N, N)




