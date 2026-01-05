#!/usr/bin/env python3
"""
Run all milestone-2 parser tests and report results.
"""

import subprocess
import sys
from pathlib import Path

def run_test(test_num):
    """Run a single test and return True if it passes."""
    input_file = f"test/milestone-2/input/test{test_num}.pas"
    expected_file = f"test/milestone-2/expected/test{test_num}.txt"

    # Check if files exist
    if not Path(input_file).exists():
        return None, "Input file not found"
    if not Path(expected_file).exists():
        return None, "Expected file not found"

    # Run the parser
    try:
        result = subprocess.run(
            ["uv", "run", "src/parser_main.py", input_file, "--check"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )

        # Check if test passed
        if "[PASS]" in result.stdout:
            return True, "PASS"
        elif "[FAIL]" in result.stdout:
            return False, "Output differs from expected"
        else:
            return False, result.stderr or "Unknown error"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    """Run all tests and report results."""
    print("Running milestone-2 parser tests...\n")

    results = {}
    passed = 0
    failed = 0
    skipped = 0

    # Auto-discover tests based on input files
    input_dir = Path("test/milestone-2/input")
    inputs = sorted(input_dir.glob("test*.pas"))

    test_nums = [int(p.stem.replace("test", "")) for p in inputs]

    for i in test_nums:
        print(f"Testing test{i}.pas...", end=" ")
        result, message = run_test(i)

        if result is None:
            print(f"SKIPPED: {message}")
            skipped += 1
            results[i] = ("SKIPPED", message)
        elif result:
            print(f"PASS")
            passed += 1
            results[i] = ("PASS", message)
        else:
            print(f"FAIL: {message}")
            failed += 1
            results[i] = ("FAIL", message)


    # Print summary
    print("\n" + "="*60)
    print(f"SUMMARY: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*60)

    if failed > 0:
        print("\nFailed tests:")
        for i, (status, msg) in results.items():
            if status == "FAIL":
                print(f"  test{i}: {msg}")

    # Exit with error code if any tests failed
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
