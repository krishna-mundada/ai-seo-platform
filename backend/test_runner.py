#!/usr/bin/env python3
"""
Test runner script for the AI SEO Platform backend.
Provides easy commands to run different test suites.
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
    else:
        print(f"❌ {description} - FAILED")
        
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run backend tests for AI SEO Platform")
    parser.add_argument("--cascade", action="store_true", help="Run CASCADE delete tests only")
    parser.add_argument("--business", action="store_true", help="Run business API tests only") 
    parser.add_argument("--content", action="store_true", help="Run content API tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = ["python", "-m", "pytest"]
    
    if args.verbose:
        base_cmd.append("-v")
    
    if args.coverage:
        base_cmd.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html"])
    
    # Determine which tests to run
    test_files = []
    
    if args.cascade:
        test_files.append("tests/api/endpoints/test_business_cascade_delete.py")
    
    if args.business:
        test_files.append("tests/api/endpoints/test_businesses.py")
    
    if args.content:
        test_files.append("tests/api/endpoints/test_content.py")
    
    if args.all or not test_files:
        test_files = ["tests/"]
    
    # Run the tests
    total_failures = 0
    
    for test_file in test_files:
        cmd = base_cmd + [test_file]
        result = run_command(cmd, f"Testing {test_file}")
        total_failures += result
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if total_failures == 0:
        print("🎉 All tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print(f"❌ {total_failures} test suite(s) failed")
    
    return total_failures


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)