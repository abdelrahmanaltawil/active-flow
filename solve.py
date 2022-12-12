import numpy as np
from scipy.fftpack import fft2, ifft2, fftfreq



N =256

# k_x = np.zeros((N, N), dtype=np.float64)
# k_y = np.zeros((N, N), dtype=np.float64)
# k_square = np.zeros((N, N), dtype=np.float64)
# deAlias = np.zeros((N, N), dtype=np.bool8)
k_inverse = np.zeros((N, N), dtype=np.float64)

# Scheme constant terms IM:Implicit, EX:Explicit 
# v_eff = np.zeros((N, N), dtype=np.float64)

# u = np.zeros((N,N), dtype=np.float64)
# v = np.zeros((N,N), dtype=np.float64)

# w_k = np.zeros((N,N), dtype=np.complex64)
# u_k = np.zeros((N,N), dtype=np.complex64)
# v_k = np.zeros((N,N), dtype=np.complex64)


# operators
# k_x= k_vectors[:,:,0]
# k_y = k_vectors[:,:,1]
k_axis = 2*np.pi*fftfreq(N, 2*np.pi/N)
k_x, k_y = np.meshgrid(k_axis, k_axis)
k_modes= np.arange(1, N/2)
k_square = k_x**2 + k_y**2
deAlias = k_square < (2/3*(N/2))**2
np.place(k_inverse, k_square != 0, k_square[k_square != 0]**-1)
k_scale_bound = np.linspace(0,np.max(np.sqrt(k_square)), N)
dk = k_scale_bound[1] - k_scale_bound[0]

v_eff = np.zeros((N, N))
v_eff[np.sqrt(k_square) < 33] = 1.1e-3
v_eff[(np.sqrt(k_square) >= 33) & (np.sqrt(k_square) <= 40)] = -5*1.1e-3
v_eff[np.sqrt(k_square) > 40] = 10*1.1e-3

w = np.random.normal(0, 1, size=(N,N))
w_k = fft2(w)

# linear -> A: `v_eff * k^2 * w_k` & non-linear -> C: `u*wx + v*wy` functions
A = lambda w_k: v_eff*k_square*w_k*deAlias
C = lambda w_k: fft2(   np.real(ifft2(1j*k_y*(w_k*k_inverse)))  * np.real(ifft2(1j*k_x*w_k))
                      + np.real(ifft2(-1j*k_x*(w_k*k_inverse))) * np.real(ifft2(1j*k_y*w_k)) )*deAlias 

# w_k = w_k*deAlias

tau = 1e-3
monitor = []
snapshots = []
for iteration in range(15000):

    w_k1 = w_k + tau*(-C(w_k) - A(w_k))
    w_k2 = 3/4.*w_k + 1/4.*w_k1 + 1/4*tau*(-C(w_k1) - A(w_k1))
    w_k = 1/3.*w_k + 2/3.*w_k2 + 2/3*tau*(-C(w_k2) - A(w_k2))        
    w_k = w_k*deAlias

    psi_k = w_k*k_inverse
    u_k = 1j*k_y*psi_k
    v_k = -1j*k_x*psi_k

    u = np.real(ifft2(u_k))
    v = np.real(ifft2(v_k))

    max_u = np.max(abs(np.sqrt(u**2 + v**2)))
    if iteration > 2500:
        tau = 1*np.min((2*np.pi/N)/max_u)


    if iteration % 100 == 0:
        circles = np.array([np.sqrt(k_square) == k for k in k_modes])
        U_k= np.abs(u_k)**2 + np.abs(v_k)**2
        E_k = 0.5*k_modes*np.sum(U_k*circles, axis=(1,2))/(dk*N**4)

        print((iteration, max_u, E_k[0]))
        monitor.append(
            (   
                iteration,
                max_u, 
                E_k[0]
            )
        )

    if iteration % 1000 == 0:
        snapshots.append(
                (
                    iteration,
                    w_k
                )
            )