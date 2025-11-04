"""Tests for 1D Hubbard model calculations."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import unittest

class TestHubbard(unittest.TestCase):
    """Test cases for 1D Hubbard model."""
    
    def test_openfermion_import(self):
        """Test that OpenFermion can be imported."""
        try:
            import openfermion
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported, "OpenFermion not installed")
        
    def test_script_exists(self):
        """Test that main script exists."""
        script_file = 'ed_1d_hubbard/run_ed_pairing_openfermion.py'
        self.assertTrue(os.path.exists(script_file))
        
    def test_hubbard_hamiltonian_basic(self):
        """Test basic properties of Hubbard Hamiltonian."""
        try:
            from openfermion import FermionOperator, hermitian_conjugated, normal_ordered
            
            # Simple 2-site Hubbard model
            t = 1.0
            U = 2.0
            
            # Hopping terms
            H_hop = FermionOperator(((0, 1), (1, 0)), -t)  # c†_0↑ c_1↑
            H_hop += FermionOperator(((1, 1), (0, 0)), -t)  # c†_1↑ c_0↑
            H_hop += FermionOperator(((2, 1), (3, 0)), -t)  # c†_0↓ c_1↓
            H_hop += FermionOperator(((3, 1), (2, 0)), -t)  # c†_1↓ c_0↓
            
            # Interaction terms
            H_int = FermionOperator(((0, 1), (0, 0), (2, 1), (2, 0)), U)  # n_0↑ n_0↓
            H_int += FermionOperator(((1, 1), (1, 0), (3, 1), (3, 0)), U)  # n_1↑ n_1↓
            
            H_total = H_hop + H_int
            
            # Test Hermiticity by checking coefficient equality
            H_conj = hermitian_conjugated(H_total)
            
            # Normal order both to ensure consistent term ordering
            H_total_ordered = normal_ordered(H_total)
            H_conj_ordered = normal_ordered(H_conj)
            
            # Check that the number of terms is the same
            self.assertEqual(len(H_total_ordered.terms), len(H_conj_ordered.terms))
            
            # For Hermitian operator, coefficients should be real
            for term, coeff in H_total_ordered.terms.items():
                # Check coefficient is real (or very close to real)
                self.assertAlmostEqual(coeff.imag, 0.0, places=10)
                # Check the term exists in conjugate with same coefficient
                if term in H_conj_ordered.terms:
                    self.assertAlmostEqual(complex(coeff), 
                                         complex(H_conj_ordered.terms[term]), 
                                         places=10)
            
        except ImportError:
            self.skipTest("OpenFermion not available")
            
    def test_hubbard_particle_number(self):
        """Test that we can create number operators."""
        try:
            from openfermion import FermionOperator
            
            # Number operator for site 0, spin up
            n_0up = FermionOperator(((0, 1), (0, 0)), 1.0)
            
            # Check it's non-empty
            self.assertGreater(len(n_0up.terms), 0)
            
        except ImportError:
            self.skipTest("OpenFermion not available")

if __name__ == '__main__':
    unittest.main()
