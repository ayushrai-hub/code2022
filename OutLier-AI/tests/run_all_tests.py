#!/usr/bin/env python3
"""
Unified test runner for OutLier-AI project.

Runs all test files found in the PythonScriptsOutlierWeeks directory.
"""

import unittest
import sys
import os
from pathlib import Path

def discover_and_run_tests():
    """Discover and run all tests in the project."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Add project root to Python path
    sys.path.insert(0, str(project_root))
    
    # Find all test files
    test_pattern = "test_*.py"
    test_files = list(project_root.rglob(test_pattern))
    
    # Filter out files in node_modules, .venv, etc.
    test_files = [
        f for f in test_files
        if '.venv' not in str(f) and 'myenv' not in str(f) and 'node_modules' not in str(f)
    ]
    
    print(f"Found {len(test_files)} test files")
    print("=" * 70)
    
    # Run tests from each directory
    results = {
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'total': 0
    }
    
    for test_file in sorted(test_files):
        test_dir = test_file.parent
        test_name = test_file.name
        
        print(f"\n{'='*70}")
        print(f"Running tests from: {test_file.relative_to(project_root)}")
        print(f"{'='*70}")
        
        # Change to test directory to handle imports
        original_cwd = os.getcwd()
        try:
            os.chdir(test_dir)
            
            # Discover and run tests
            loader = unittest.TestLoader()
            suite = loader.discover(start_dir=str(test_dir), pattern=test_name)
            
            runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
            result = runner.run(suite)
            
            results['passed'] += result.testsRun - len(result.failures) - len(result.errors)
            results['failed'] += len(result.failures)
            results['errors'] += len(result.errors)
            results['total'] += result.testsRun
            
        except Exception as e:
            print(f"ERROR running {test_file}: {e}")
            results['errors'] += 1
        finally:
            os.chdir(original_cwd)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Errors: {results['errors']}")
    print("=" * 70)
    
    return results['failed'] + results['errors'] == 0

if __name__ == '__main__':
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)
