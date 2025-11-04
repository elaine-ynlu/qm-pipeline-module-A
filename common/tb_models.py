import numpy as np

def tb_2orbital_dxz_dyz(kx, ky, pars):
    t1,t2,t3,txy,mu = pars["t1"], pars["t2"], pars["t3"], pars["txy"], pars["mu"]
    eps_xz = -2*t1*np.cos(kx) - 2*t2*np.cos(ky) - 4*t3*np.cos(kx)*np.cos(ky) - mu
    eps_yz = -2*t2*np.cos(kx) - 2*t1*np.cos(ky) - 4*t3*np.cos(kx)*np.cos(ky) - mu
    v_xy = -4*txy*np.sin(kx)*np.sin(ky)
    H = np.array([[eps_xz, v_xy],[v_xy, eps_yz]])
    return H

def band_2d(pars, nk=201):
    ks = np.linspace(-np.pi, np.pi, nk)
    e1 = np.zeros((nk,nk)); e2 = np.zeros_like(e1)
    for i,kx in enumerate(ks):
        for j,ky in enumerate(ks):
            w,_ = np.linalg.eigh(tb_2orbital_dxz_dyz(kx,ky,pars))
            e1[i,j], e2[i,j] = w
    return ks, e1, e2