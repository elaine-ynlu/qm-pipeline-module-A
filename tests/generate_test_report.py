#!/usr/bin/env python
"""Generate a comprehensive test report."""

import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_report():
    """Generate test report."""
    print("="*70)
    print("CONDENSED MATTER TIGHT-BINDING MODELS - TEST REPORT")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check which modules are available
    modules_status = {
        'numpy': False,
        'scipy': False,
        'matplotlib': False,
        'openfermion': False,
        'yaml': False
    }
    
    for module in modules_status:
        try:
            __import__(module)
            modules_status[module] = True
        except ImportError:
            modules_status[module] = False
    
    print("Module Availability:")
    for module, available in modules_status.items():
        status = "✓" if available else "✗"
        print(f"  {status} {module}")
    print()
    
    # Run tests
    loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    success_count = result.testsRun - len(result.failures) - len(result.errors)
    success_rate = (success_count / result.testsRun * 100) if result.testsRun > 0 else 0
    
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {success_count} ({success_rate:.1f}%)")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if success_rate >= 90:
        print("\n✅ EXCELLENT: >90% tests passing")
    elif success_rate >= 70:
        print("\n⚠️  GOOD: >70% tests passing")
    else:
        print("\n❌ NEEDS ATTENTION: <70% tests passing")
    
    print("="*70)
    
    # Write report to file
    with open('tests/test_report.txt', 'w') as f:
        f.write(f"Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n")
        f.write(f"Tests Run: {result.testsRun}\n")
        f.write(f"Passed: {success_count}\n")
        f.write(f"Failed: {len(result.failures)}\n")
        f.write(f"Errors: {len(result.errors)}\n")
    
    print("\nReport saved to: tests/test_report.txt")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = generate_report()
    sys.exit(exit_code)
