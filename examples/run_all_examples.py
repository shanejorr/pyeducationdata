"""Run all example scripts to test the package.

This script runs all numbered examples (01-05) in sequence.
Use this to quickly test that the package is working correctly.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_example(script_path):
    """Run a single example script and return success status."""
    print("\n" + "=" * 80)
    print(f"Running: {script_path.name}")
    print("=" * 80)

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout per script
        )

        elapsed = time.time() - start_time

        # Print the output
        output = result.stdout + result.stderr
        print(output)

        # Check for unexpected errors in the output
        # Don't count intentional error examples in 05_error_handling.py
        is_error_handling_example = script_path.name == "05_error_handling.py"

        if not is_error_handling_example:
            error_indicators = [
                "✗ Error:",
                "Error: Endpoint not found (404):",
                "Error: Server error (500):",
            ]

            has_unexpected_errors = any(indicator in output for indicator in error_indicators)

            if has_unexpected_errors:
                print(f"\n✗ {script_path.name} completed with errors in {elapsed:.1f}s")
                return False

        if result.returncode == 0:
            print(f"\n✓ {script_path.name} completed successfully in {elapsed:.1f}s")
            return True
        else:
            print(f"\n✗ {script_path.name} failed with return code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n✗ {script_path.name} timed out (>2 minutes)")
        return False
    except Exception as e:
        print(f"\n✗ {script_path.name} failed with error: {e}")
        return False


def main():
    """Run all numbered example scripts."""
    examples_dir = Path(__file__).parent

    # Find all numbered example scripts
    example_scripts = sorted(examples_dir.glob("0*.py"))

    if not example_scripts:
        print("No example scripts found!")
        return 1

    print("=" * 80)
    print(f"pyeducationdata Example Test Runner")
    print("=" * 80)
    print(f"\nFound {len(example_scripts)} example scripts")
    print("\nNote: These examples make real API calls and may take several minutes.")
    print("Press Ctrl+C at any time to stop.\n")

    input("Press Enter to continue or Ctrl+C to cancel...")

    results = {}
    total_start = time.time()

    for script in example_scripts:
        success = run_example(script)
        results[script.name] = success

    total_elapsed = time.time() - total_start

    # Print summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed

    for script_name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {script_name}")

    print(f"\nTotal: {passed}/{len(results)} passed, {failed}/{len(results)} failed")
    print(f"Total time: {total_elapsed:.1f}s ({total_elapsed/60:.1f} minutes)")

    if failed == 0:
        print("\n🎉 All examples completed successfully!")
        return 0
    else:
        print(f"\n⚠️  {failed} example(s) failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
