# env imports
import numpy as np
import scipy.fftpack as scipy

# local imports
import helpers.register as re


def stepping_scheme(w_k: np.ndarray, tau: float, STEPPING_SCHEME: str, A: callable, C: callable, deAlias: np.ndarray) -> np.ndarray:
    '''
    Placeholder
    '''

    if STEPPING_SCHEME == "RK3":
        w_k1 = w_k + tau*(-C(w_k) - A(w_k))
        w_k2 = 3/4.*w_k + 1/4.*w_k1 + 1/4*tau*(-C(w_k1) - A(w_k1))
        w_k = 1/3.*w_k + 2/3.*w_k2 + 2/3*tau*(-C(w_k2) - A(w_k2))        

    return w_k*deAlias


def controller(courant: float, h: float, max_u: np.ndarray) -> float:
    '''
    Placeholder
    '''

    tau = courant*np.min(h/max_u)
    
    return tau


def energy_calculation(k_norm: np.ndarray, dk: float, N: int, U_k: np.ndarray) -> np.ndarray:
    '''
    Placeholder
    '''

    circle = (k_norm >= 1) & (k_norm <= 2)
    E_k_1 = 0.5*np.sum(U_k[circle])/(dk*N**4)


    return E_k_1


def velocity_calculation(w_k: np.ndarray, k_x: np.ndarray, k_y: np.ndarray, k_inverse: np.ndarray) -> tuple[np.ndarray]:
    '''
    Placeholder
    '''
    
    psi_k = w_k*k_inverse
    u_k = 1j*k_y*psi_k
    v_k = -1j*k_x*psi_k

    u = np.real(scipy.ifft2(u_k))
    v = np.real(scipy.ifft2(v_k))

    return u, v, u_k, v_k