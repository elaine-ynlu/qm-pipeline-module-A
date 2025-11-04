"""Tests for FeSe tight-binding model."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import unittest
import yaml

class TestFeSe(unittest.TestCase):
    """Test cases for FeSe calculations."""
    
    def test_params_file_exists(self):
        """Test that parameter file exists."""
        param_file = 'fe_se_tb/fe_se_params.yaml'
        self.assertTrue(os.path.exists(param_file))
        
    def test_params_file_valid(self):
        """Test that parameter file is valid YAML."""
        param_file = 'fe_se_tb/fe_se_params.yaml'
        if os.path.exists(param_file):
            with open(param_file, 'r') as f:
                try:
                    params = yaml.safe_load(f)
                    self.assertIsInstance(params, dict)
                except yaml.YAMLError:
                    self.fail("Invalid YAML file")
    
    def test_run_tb_exists(self):
        """Test that main script exists."""
        script_file = 'fe_se_tb/run_tb.py'
        self.assertTrue(os.path.exists(script_file))
        
    def test_output_directory(self):
        """Test that output directory structure exists."""
        self.assertTrue(os.path.exists('fe_se_tb'))
        self.assertTrue(os.path.exists('fe_se_tb/figs'))

if __name__ == '__main__':
    unittest.main()
