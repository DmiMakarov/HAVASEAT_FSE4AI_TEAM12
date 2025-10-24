#!/usr/bin/env python3
"""
Test runner script for the FastAPI backend
"""
import subprocess
import sys
import os


def run_tests():
    """Run all tests with pytest"""
    print("🧪 Running FastAPI Backend Tests")
    print("=" * 50)

    # Change to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)

    # Use the virtual environment Python if available
    python_cmd = "python"
    venv_python = os.path.join(os.path.dirname(backend_dir), ".venv", "bin", "python")
    if os.path.exists(venv_python):
        python_cmd = venv_python

    # Run different test categories
    test_commands = [
        ("Unit Tests", [python_cmd, "-m", "pytest", "tests/test_model.py", "-v", "-m", "unit"]),
        ("API Tests", [python_cmd, "-m", "pytest", "tests/test_api.py", "-v", "-m", "api"]),
        ("Integration Tests", [python_cmd, "-m", "pytest", "tests/test_api.py", "-v", "-m", "integration"]),
        ("Performance Tests", [python_cmd, "-m", "pytest", "tests/test_performance.py", "-v", "-m", "performance"]),
        ("All Tests", [python_cmd, "-m", "pytest", "tests/", "-v"]),
    ]

    results = {}

    for test_name, command in test_commands:
        print(f"\n🔍 Running {test_name}...")
        print("-" * 30)

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
            results[test_name] = {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}

            if result.returncode == 0:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)

        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name} TIMED OUT")
            results[test_name] = {"returncode": -1, "stdout": "", "stderr": "Timeout"}
        except Exception as e:
            print(f"💥 {test_name} ERROR: {e}")
            results[test_name] = {"returncode": -1, "stdout": "", "stderr": str(e)}

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result["returncode"] == 0 else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result["returncode"] == 0:
            passed += 1

    print(f"\nResults: {passed}/{total} test suites passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
