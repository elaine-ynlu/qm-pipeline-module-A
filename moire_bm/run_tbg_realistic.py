#!/usr/bin/env python
"""
Twisted Bilayer Graphene (TBG) Band Structure Calculator
=========================================================
Calculate and visualize the electronic band structure of TBG
using the Bistritzer-MacDonald continuum model.

References:
    - Bistritzer & MacDonald, PNAS 2011
    - Cao et al., Nature 2018 (Magic angle discovery)
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eigvalsh
import os

def make_TBG_hamiltonian(kx, ky, theta_deg=1.1, use_realistic_params=True):
    """
    构建TBG哈密顿量，使用实际物理参数
    """
    theta = np.radians(theta_deg)
    
    if use_realistic_params:
        # 实际物理参数（来自 Bistritzer & MacDonald 2011）
        # 石墨烯晶格常数 a = 2.46 Å
        a = 2.46  # Angstrom
        vF = 1.0e6  # m/s = 10^6 m/s
        hbar = 6.582e-16  # eV·s
        hbar_vF = hbar * vF * 1e10 / a  # 转换为 eV (using a in Angstrom)
        hbar_vF = 2.1354  # eV (标准值)
        
        # 层间耦合参数
        w0 = 0.0797  # eV (AA stacking)
        w1 = 0.0975  # eV (AB stacking)
    else:
        # 简化参数用于测试
        hbar_vF = 1.0
        w0 = 0.0
        w1 = 0.11
    
    # Pauli matrices
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s0 = np.eye(2, dtype=complex)
    
    # 旋转矩阵
    def rot(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s], [s, c]])
    
    # 两层的旋转
    R1 = rot(-theta/2)  # 顶层
    R2 = rot(theta/2)   # 底层
    
    # 动量
    k = np.array([kx, ky])
    k1 = R1 @ k
    k2 = R2 @ k
    
    # 4×4 哈密顿量
    H = np.zeros((4, 4), dtype=complex)
    
    # 层内项（Dirac哈密顿量）
    H[0:2, 0:2] = hbar_vF * (k1[0] * sx + k1[1] * sy)  # 顶层
    H[2:4, 2:4] = hbar_vF * (k2[0] * sx + k2[1] * sy)  # 底层
    
    # 层间耦合
    T = w0 * s0 + w1 * sx  # 简化的耦合矩阵
    H[0:2, 2:4] = T
    H[2:4, 0:2] = T.conj().T
    
    return H

def get_moire_BZ_path(theta_deg, nk=100):
    """
    生成moiré布里渊区的高对称路径
    """
    theta = np.radians(theta_deg)
    
    # 石墨烯的K点（倒格矢单位）
    K_graphene = 4*np.pi/(3*np.sqrt(3))  # |K| for graphene
    
    # Moiré 布里渊区大小
    G_M = 2 * K_graphene * np.sin(theta/2)
    
    # 高对称点（在moiré BZ中）
    Gamma = np.array([0, 0])
    K_M = G_M * np.array([2/3, 0])  # Moiré BZ的K点
    M_M = G_M * np.array([1/2, 0])  # Moiré BZ的M点
    
    # 生成路径 Γ → K → M → Γ
    path = []
    labels = []
    
    # Γ to K
    for i in range(nk//3):
        t = i / (nk//3)
        path.append((1-t)*Gamma + t*K_M)
    labels.append(nk//3)
    
    # K to M  
    for i in range(nk//3):
        t = i / (nk//3)
        path.append((1-t)*K_M + t*M_M)
    labels.append(2*nk//3)
    
    # M to Γ
    for i in range(nk//3 + 1):
        t = i / (nk//3)
        path.append((1-t)*M_M + t*Gamma)
    
    return np.array(path), labels

def calculate_band_structure(theta_deg, nk=150, use_realistic=True):
    """
    计算完整能带结构
    """
    k_path, labels = get_moire_BZ_path(theta_deg, nk)
    
    bands = []
    for k in k_path:
        H = make_TBG_hamiltonian(k[0], k[1], theta_deg, use_realistic)
        eigvals = np.sort(eigvalsh(H))
        bands.append(eigvals)
    
    return np.array(bands), k_path, labels

def plot_bands_comparison():
    """
    比较不同角度的能带结构
    """
    angles = [0.5, 1.05, 1.5, 2.0]  # 魔角在1.05度附近
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for idx, theta in enumerate(angles):
        bands, k_path, labels = calculate_band_structure(theta, nk=200, use_realistic=True)
        
        ax = axes[idx]
        x = np.arange(len(k_path))
        
        # 画所有能带
        for i in range(bands.shape[1]):
            color = 'red' if i in [1, 2] else 'blue'  # 中间两条带标红
            linewidth = 2 if i in [1, 2] else 1
            ax.plot(x, bands[:, i], color=color, linewidth=linewidth)
        
        # 标记高对称点
        ax.axvline(x=labels[0], color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=labels[1], color='gray', linestyle='--', alpha=0.5)
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        
        ax.set_xticks([0, labels[0], labels[1], len(x)-1])
        ax.set_xticklabels(['Γ', 'K', 'M', 'Γ'])
        ax.set_ylabel('Energy (eV)')
        ax.set_title(f'θ = {theta}°')
        ax.set_ylim(-0.3, 0.3)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('TBG Band Structure at Different Twist Angles (Realistic Parameters)')
    plt.tight_layout()
    return fig

def calculate_bandwidth_correct(theta_deg, use_realistic=True):
    """
    正确计算平带带宽
    """
    bands, _, _ = calculate_band_structure(theta_deg, nk=200, use_realistic=use_realistic)
    
    # 对于4带模型，中间两条是平带
    band1 = bands[:, 1]  # 价带顶
    band2 = bands[:, 2]  # 导带底
    
    # 平带带宽定义为这两条带的总宽度
    bandwidth = max(band2) - min(band1)
    
    return bandwidth

def main():
    os.makedirs("figs", exist_ok=True)
    
    print("="*60)
    print("TBG Band Structure Calculation with Realistic Parameters")
    print("="*60)
    
    # 1. 画不同角度的能带结构
    print("\n1. Plotting band structures at different angles...")
    fig = plot_bands_comparison()
    plt.savefig("figs/tbg_bands_realistic.png", dpi=150)
    plt.show()
    
    # 2. 计算带宽vs角度
    print("\n2. Calculating bandwidth vs twist angle...")
    
    # 角度范围（魔角在1.05度附近）
    angles = np.concatenate([
        np.linspace(0.3, 0.9, 10),
        np.linspace(0.9, 1.2, 20),  # 魔角附近加密
        np.linspace(1.2, 2.5, 15)
    ])
    
    bandwidths_realistic = []
    bandwidths_simple = []
    
    for theta in angles:
        bw_real = calculate_bandwidth_correct(theta, use_realistic=True)
        bw_simple = calculate_bandwidth_correct(theta, use_realistic=False)
        bandwidths_realistic.append(bw_real)
        bandwidths_simple.append(bw_simple)
        print(f"θ = {theta:.2f}°: BW(realistic) = {bw_real*1000:.2f} meV, "
              f"BW(simple) = {bw_simple:.3f}")
    
    bandwidths_realistic = np.array(bandwidths_realistic)
    bandwidths_simple = np.array(bandwidths_simple)
    
    # 找到最小值（魔角）
    min_idx_real = np.argmin(bandwidths_realistic)
    min_idx_simple = np.argmin(bandwidths_simple)
    
    print(f"\nRealistic parameters:")
    print(f"  Magic angle: θ = {angles[min_idx_real]:.3f}°")
    print(f"  Minimum bandwidth: {bandwidths_realistic[min_idx_real]*1000:.2f} meV")
    
    print(f"\nSimple parameters:")
    print(f"  Magic angle: θ = {angles[min_idx_simple]:.3f}°")
    print(f"  Minimum bandwidth: {bandwidths_simple[min_idx_simple]:.4f}")
    
    # 3. 画带宽vs角度
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 实际参数结果
    ax = axes[0]
    ax.plot(angles, bandwidths_realistic*1000, 'b.-', markersize=4, label='Bandwidth')
    ax.axvline(x=angles[min_idx_real], color='r', linestyle='--', 
               alpha=0.5, label=f'Magic angle = {angles[min_idx_real]:.2f}°')
    ax.set_xlabel('Twist angle (degrees)')
    ax.set_ylabel('Bandwidth (meV)')
    ax.set_title('TBG Bandwidth (Realistic Parameters)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(0.3, 2.5)
    
    # 简化参数结果（用于对比）
    ax = axes[1]
    ax.plot(angles, bandwidths_simple, 'g.-', markersize=4, label='Bandwidth')
    ax.axvline(x=angles[min_idx_simple], color='r', linestyle='--',
               alpha=0.5, label=f'Magic angle = {angles[min_idx_simple]:.2f}°')
    ax.set_xlabel('Twist angle (degrees)')
    ax.set_ylabel('Bandwidth (arb. units)')
    ax.set_title('TBG Bandwidth (Simplified Parameters)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(0.3, 2.5)
    
    plt.tight_layout()
    plt.savefig("figs/tbg_bandwidth_analysis.png", dpi=150)
    plt.show()
    
    # 保存数据
    np.savetxt("figs/bandwidth_data_realistic.txt",
               np.column_stack([angles, bandwidths_realistic*1000]),
               header="angle_deg bandwidth_meV")
    
    print("\n" + "="*60)
    print("Analysis complete. Results saved in figs/")
    print("="*60)

if __name__ == "__main__":
    main()
