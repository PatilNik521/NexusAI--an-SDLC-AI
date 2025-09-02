#!/usr/bin/env python
# AI-Powered SDLC System - Test Runner

import unittest
import os
import sys
import argparse

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from test_core_functionality import CoreFunctionalityTests

# End-to-end tests are imported conditionally based on command line arguments

def run_tests(test_type='all', verbose=False):
    """Run the specified tests.
    
    Args:
        test_type (str): Type of tests to run ('unit', 'e2e', or 'all')
        verbose (bool): Whether to show verbose output
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add tests based on the test type
    if test_type in ['unit', 'all']:
        print("\n=== Running Unit Tests ===")
        test_suite.addTest(unittest.makeSuite(CoreFunctionalityTests))
    
    if test_type in ['e2e', 'all']:
        print("\n=== Running End-to-End Tests ===")
        try:
            from test_end_to_end import EndToEndTests
            test_suite.addTest(unittest.makeSuite(EndToEndTests))
        except ImportError as e:
            print(f"Warning: Could not import End-to-End tests: {e}")
            print("Skipping End-to-End tests. Make sure Selenium and WebDriver are installed.")
    
    if test_type == 'ui':
        print("\n=== Running UI Tests ===")
        print("UI tests must be run with Jest. Please use 'npm test' to run UI tests.")
        return True
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = test_runner.run(test_suite)
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    # Return True if all tests passed
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Parse command line arguments and run tests."""
    parser = argparse.ArgumentParser(description='Run tests for the AI-Powered SDLC System')
    parser.add_argument('--type', choices=['unit', 'e2e', 'ui', 'all'], default='all',
                        help='Type of tests to run (default: all)')
    parser.add_argument('--verbose', action='store_true',
                        help='Show verbose output')
    args = parser.parse_args()
    
    # Run the tests
    success = run_tests(args.type, args.verbose)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()