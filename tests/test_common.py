"""Tests for common utilities."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import unittest

class TestCommon(unittest.TestCase):
    """Test cases for common utilities."""
    
    def test_common_module_exists(self):
        """Test that common module can be imported."""
        try:
            import common
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)
        
    def test_tb_models_exists(self):
        """Test that tb_models file exists."""
        self.assertTrue(os.path.exists('common/tb_models.py'))
        
    def test_pauli_matrices(self):
        """Test Pauli matrix properties."""
        # Define Pauli matrices
        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)
        s0 = np.eye(2, dtype=complex)
        
        # Test commutation relations
        # [sx, sy] = 2i*sz
        comm_xy = sx @ sy - sy @ sx
        np.testing.assert_allclose(comm_xy, 2j * sz)
        
        # Test anticommutation relations (修正: sx^2 = I)
        # {sx, sx} = 2*sx^2 = 2*I
        anticomm_xx = sx @ sx + sx @ sx
        np.testing.assert_allclose(anticomm_xx, 2 * s0)
        
        # Test that Pauli matrices square to identity
        np.testing.assert_allclose(sx @ sx, s0)
        np.testing.assert_allclose(sy @ sy, s0)
        np.testing.assert_allclose(sz @ sz, s0)
        
        # Test trace properties
        self.assertAlmostEqual(np.trace(sx), 0)
        self.assertAlmostEqual(np.trace(sy), 0)
        self.assertAlmostEqual(np.trace(sz), 0)
        
    def test_rotation_matrix(self):
        """Test 2D rotation matrix properties."""
        def rot(angle):
            c, s = np.cos(angle), np.sin(angle)
            return np.array([[c, -s], [s, c]])
        
        # Test identity at angle=0
        R0 = rot(0)
        np.testing.assert_allclose(R0, np.eye(2))
        
        # Test rotation by π/2 (加入容差处理浮点误差)
        R90 = rot(np.pi/2)
        v = np.array([1, 0])
        v_rot = R90 @ v
        np.testing.assert_allclose(v_rot, np.array([0, 1]), atol=1e-15)
        
        # Test inverse property
        angle = 0.5
        R = rot(angle)
        R_inv = rot(-angle)
        np.testing.assert_allclose(R @ R_inv, np.eye(2), atol=1e-15)

if __name__ == '__main__':
    unittest.main()
