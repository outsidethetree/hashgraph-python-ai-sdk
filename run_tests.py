#!/usr/bin/env python3
import subprocess
import sys
import os

if __name__ == "__main__":
    # Add src directory to Python path so tests can import modules
    env = os.environ.copy()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{src_path}:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = src_path
    
    result = subprocess.run(["python3", "-m", "pytest", "tests/", "-v", "--tb=short", "--color=yes"], 
                          capture_output=False, env=env)
    sys.exit(result.returncode) 