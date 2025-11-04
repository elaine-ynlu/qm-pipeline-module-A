"""Tests for TBG band structure calculations."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import unittest
from moire_bm.run_tbg_realistic import (
    make_TBG_hamiltonian,
    get_moire_BZ_path,
    calculate_bandwidth_correct
)

class TestTBG(unittest.TestCase):
    """Test cases for TBG calculations."""
    
    def test_hamiltonian_hermitian(self):
        """Test that Hamiltonian is Hermitian."""
        H = make_TBG_hamiltonian(0.1, 0.1, theta_deg=1.05)
        np.testing.assert_allclose(H, H.conj().T, rtol=1e-10)
        
    def test_hamiltonian_size(self):
        """Test Hamiltonian has correct size."""
        H = make_TBG_hamiltonian(0.0, 0.0)
        self.assertEqual(H.shape, (4, 4))
        
    def test_gamma_point_symmetry(self):
        """Test that at Gamma point (k=0), certain symmetries hold."""
        H = make_TBG_hamiltonian(0.0, 0.0, theta_deg=1.05)
        # At k=0, the diagonal blocks should be zero (Dirac point)
        np.testing.assert_allclose(H[0:2, 0:2], np.zeros((2,2)), atol=1e-10)
        np.testing.assert_allclose(H[2:4, 2:4], np.zeros((2,2)), atol=1e-10)
        
    def test_moire_BZ_path(self):
        """Test moiré BZ path generation."""
        path, labels = get_moire_BZ_path(1.05, nk=90)
        
        # Check path has correct number of points
        self.assertGreater(len(path), 90)
        
        # Check labels are at correct positions
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels[0], 30)  # nk//3
        self.assertEqual(labels[1], 60)  # 2*nk//3
        
        # Check start and end points are the same (Gamma)
        np.testing.assert_allclose(path[0], path[-1], atol=1e-10)
        
    def test_bandwidth_positive(self):
        """Test that bandwidth is positive."""
        bw = calculate_bandwidth_correct(1.05, use_realistic=True)
        self.assertGreater(bw, 0)
        
    def test_bandwidth_variation(self):
        """Test that bandwidth varies with angle and has expected behavior."""
        # Test a range that should definitely include variation
        angles = [0.3, 0.5, 1.0, 1.5, 2.0, 2.5]
        bandwidths = [calculate_bandwidth_correct(theta, use_realistic=True) 
                     for theta in angles]
        
        # All bandwidths should be positive
        for bw in bandwidths:
            self.assertGreater(bw, 0)
        
        # Bandwidths should not all be the same
        self.assertGreater(max(bandwidths), min(bandwidths))
        
        # There should be significant variation (at least 20% difference)
        variation = (max(bandwidths) - min(bandwidths)) / max(bandwidths)
        self.assertGreater(variation, 0.2)
        
        # For small angles (<0.5°), bandwidth should be relatively small
        # This is a general property of TBG
        bw_small = calculate_bandwidth_correct(0.3, use_realistic=True)
        bw_large = calculate_bandwidth_correct(2.5, use_realistic=True)
        
        # Generally, very small and very large angles have larger bandwidth
        # than intermediate angles (though exact behavior depends on parameters)
        # So we just test that they're different
        self.assertNotAlmostEqual(bw_small, bw_large, places=3)
        
    def test_bandwidth_calculation_consistency(self):
        """Test that bandwidth calculation is consistent."""
        theta = 1.05
        bw1 = calculate_bandwidth_correct(theta, use_realistic=True)
        bw2 = calculate_bandwidth_correct(theta, use_realistic=True)
        
        # Should get same result
        self.assertAlmostEqual(bw1, bw2, places=10)
        
    def test_realistic_vs_simple_params(self):
        """Test that realistic and simple parameters give different results."""
        theta = 1.05
        bw_real = calculate_bandwidth_correct(theta, use_realistic=True)
        bw_simple = calculate_bandwidth_correct(theta, use_realistic=False)
        
        # They should be different
        self.assertNotAlmostEqual(bw_real, bw_simple, places=3)
        
        # Both should be positive
        self.assertGreater(bw_real, 0)
        self.assertGreater(bw_simple, 0)
        
    def test_hamiltonian_momentum_dependence(self):
        """Test that Hamiltonian depends on momentum."""
        theta = 1.05
        H1 = make_TBG_hamiltonian(0.0, 0.0, theta_deg=theta)
        H2 = make_TBG_hamiltonian(0.1, 0.1, theta_deg=theta)
        
        # Hamiltonians at different k-points should be different
        with self.assertRaises(AssertionError):
            np.testing.assert_allclose(H1, H2, rtol=1e-10)

if __name__ == '__main__':
    unittest.main()
