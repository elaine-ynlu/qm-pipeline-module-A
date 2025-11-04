import numpy as np, matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh
from openfermion import FermionOperator, jordan_wigner, get_sparse_operator, normal_ordered

def hubbard_1d(L=6, t=1.0, U=0.0, periodic=True):
    H = FermionOperator()
    def idx(i, s): return 2*i + s  # s=0 up, 1 down
    # hopping
    for i in range(L):
        j = (i+1) % L if periodic else i+1
        if j >= L: break
        for s in (0,1):
            H += FermionOperator(((idx(i,s),1),(idx(j,s),0)), -t)
            H += FermionOperator(((idx(j,s),1),(idx(i,s),0)), -t)
    # on-site U
    for i in range(L):
        up, dn = idx(i,0), idx(i,1)
        H += FermionOperator(((up,1),(up,0),(dn,1),(dn,0)), U)
    return normal_ordered(H)

def ground_state(L, H_fermion):
    op = get_sparse_operator(jordan_wigner(H_fermion), n_qubits=2*L)
    e0, vecs = eigsh(op, k=1, which='SA')
    return float(e0[0]), vecs[:,0]

def spair_q0(L, v):
    # S_pair(q=0) = (1/L^2) sum_{i,j} <Δ_i^† Δ_j>, Δ_i = c_{i,down} c_{i,up}
    from openfermion import FermionOperator
    dim = v.shape[0]
    S = 0.0
    def idx(i,s): return 2*i + s
    for i in range(L):
        for j in range(L):
            op_ij = FermionOperator(((idx(i,0),1),(idx(i,1),1),(idx(j,1),0),(idx(j,0),0)))
            sop = get_sparse_operator(jordan_wigner(op_ij), n_qubits=2*L)
            S += (v.conj().T @ (sop @ v)).real
    return S / (L*L)

if __name__ == "__main__":
    L=6; periodic=True
    Us = np.linspace(-4, 4, 9)
    Sp = []
    for U in Us:
        H = hubbard_1d(L=L, t=1.0, U=U, periodic=periodic)
        e0, v0 = ground_state(L, H)
        S0 = spair_q0(L, v0)
        Sp.append(S0)
        print(f"U={U:+.2f}, E0={e0:.4f}, S_pair(0)={S0:.4f}")
    Sp = np.array(Sp)
    plt.figure(figsize=(5,3))
    plt.plot(Us, Sp, '-o')
    plt.xlabel("U"); plt.ylabel("S_pair(q=0)")
    plt.title(f"1D Hubbard (L={L}) pairing structure factor")
    plt.tight_layout(); plt.savefig("figs/hubbard_L6_Spair_vs_U.png", dpi=160)
    print("Saved figs/hubbard_L6_Spair_vs_U.png")