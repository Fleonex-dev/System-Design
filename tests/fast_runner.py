
import sys
import os
import runpy
from unittest.mock import MagicMock

# ==========================================
# 🚀 FAST RUNNER (Patches time.sleep)
# ==========================================
# Usage: python tests/fast_runner.py <path_to_script>
#
# This script:
# 1. Patches time.sleep to be instant.
# 2. Patches built-in 'input' to avoid hanging.
# 3. Executes the target script in the same process.

def mock_sleep(seconds):
    # Log that we skipped a sleep
    # print(f"   ⏩ Fast-forwarded sleep({seconds}s)")
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fast_runner.py <script_path>")
        sys.exit(1)

    target_script = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(target_script))
    
    # 1. Setup Path so relative imports work
    sys.path.insert(0, script_dir)
    
    # 2. Patch Time and Input
    import time
    time.sleep = mock_sleep
    
    import builtins
    builtins.input = MagicMock(return_value="mock_input")
    
    print(f"⚡ execution: {target_script}")
    
    # 3. Execute
    try:
        runpy.run_path(target_script, run_name="__main__")
    except SystemExit as e:
        # Some scripts might call sys.exit(), which is fine
        if e.code != 0:
            raise e
    except Exception as e:
        print(f"❌ Crash in {target_script}")
        raise e
