
import pytest
import subprocess
import glob
import os
import sys

# Define the root directories to search for lessons
# We exclude venv, tests, and root scripts like learn.py for now (handle separately if needed)
LESSON_DIRS = [
    "01_python_essentials",
    "02_lld_principles",
    "03_hld_concepts",
    "04_advanced_ai_arch",
    "05_interview_prep"
]

def get_all_python_files():
    files = []
    root = os.getcwd()
    for d in LESSON_DIRS:
        # Recursive glob
        path = os.path.join(root, d, "**", "*.py")
        found = glob.glob(path, recursive=True)
        files.extend(found)
    
    # Filter out empty __init__.py files if any, although running them is harmless
    # Filter out 'bad.py' files? 
    # Decision: 'bad.py' usually contains buggy code or race conditions BUT they should strictly run without crashing 
    # unless they are explicitly designed to raise an Uncaught Exception. 
    # Most of our bad.py print an error or handle it. 
    # Exception: Some chaos/race condition scripts might fail probabilistically.
    # Let's exclude files known to crash by design if any. 
    # Reviewing the code: Most bad.py just print "Failed".
    
    return sorted(files)

ALL_LESSONS = get_all_python_files()

@pytest.mark.parametrize("filepath", ALL_LESSONS)
def test_simulation_runs_without_crashing(filepath):
    """
    Runs every lesson script in a subprocess to ensure:
    1. No Syntax Errors.
    2. No Runtime Errors (Exit Code 0).
    3. Runs within a reasonable timeout.
    """
    
    # Skip known "infinite loop" or "interactive" scripts if any.
    # Currently almost all scripts are self-terminating simulations.
    
    relative_path = os.path.relpath(filepath)
    print(f"Testing: {relative_path}")
    
    try:
        # We assume python3 is available. Using sys.executable ensures we use the same venv.
        # Timeout: Some scripts run for 5-10 seconds (simulated delays).
        # We give a generous 30s buffer.
        # Use the fast_runner.py wrapper to mock sleep/input
        runner_path = os.path.join(os.getcwd(), "tests/fast_runner.py")
        
        subprocess.run(
            [sys.executable, runner_path, filepath], 
            check=True, 
            capture_output=True, 
            timeout=10, # Reduced timeout since sleeps are mocked!
            cwd=os.path.dirname(filepath)
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {relative_path} timed out after 10s.")
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode()
        stdout = e.stdout.decode()
        pytest.fail(f"Script {relative_path} crashed with Exit Code {e.returncode}.\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
