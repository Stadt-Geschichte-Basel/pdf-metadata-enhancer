#!/usr/bin/env python3
"""Run all tests for pdf-metadata-enhancer."""

import subprocess
import sys
from pathlib import Path


def run_test(test_file):
    """Run a single test file."""
    print(f"\n{'=' * 60}")
    print(f"Running: {test_file}")
    print("=" * 60)

    result = subprocess.run([sys.executable, test_file], capture_output=False)

    if result.returncode != 0:
        print(f"\n✗ Test failed: {test_file}")
        return False

    return True


def main():
    """Run all tests."""
    test_dir = Path(__file__).parent / "test"
    test_files = sorted(test_dir.glob("test_*.py"))

    if not test_files:
        print("No test files found!")
        sys.exit(1)

    print("PDF Metadata Enhancer - Test Suite")
    print("=" * 60)
    print(f"Found {len(test_files)} test file(s)")

    failed_tests = []

    for test_file in test_files:
        if not run_test(test_file):
            failed_tests.append(test_file.name)

    print(f"\n{'=' * 60}")
    print("Test Summary")
    print("=" * 60)
    print(f"Total tests: {len(test_files)}")
    print(f"Passed: {len(test_files) - len(failed_tests)}")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nFailed tests:")
        for test in failed_tests:
            print(f"  - {test}")
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
