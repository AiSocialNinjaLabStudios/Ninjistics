import subprocess
import time
import json
import os
import datetime
from pathlib import Path

# ==========================================
# CONFIGURATION: THE CONTESTANTS
# ==========================================
# Define the languages and the commands to run them.
# 'cmd': The command to execute (as a list).
# 'cwd': The directory where the code lives (relative to repo root).
CONTESTANTS = [
    {
        "name": "Python",
        "cmd": ["python", "main.py"],
        "cwd": "benchmarks/python_test"
    },
    {
        "name": "Node.js",
        "cmd": ["node", "index.js"],
        "cwd": "benchmarks/node_test"
    },
    {
        "name": "Go",
        "cmd": ["go", "run", "."],
        "cwd": "benchmarks/go_test"
    },
    {
        "name": "Rust (Release)",
        # Note: Rust usually needs a build step first, or use 'cargo run --release'
        "cmd": ["cargo", "run", "--release", "--quiet"],
        "cwd": "benchmarks/rust_test"
    },
    {
        "name": "C++",
        # Assumes you have a compiled executable named 'app'
        "cmd": ["./app"], 
        "cwd": "benchmarks/cpp_test"
    }
]

RESULTS_FILE = "results/battle_results.json"

def ensure_directories():
    """Create the results directory if it doesn't exist."""
    Path("results").mkdir(exist_ok=True)

def run_benchmark(contestant):
    """Runs a single contestant and measures execution time."""
    print(f"--- ⚔️  Starting Round: {contestant['name']} ---")
    
    # Check if directory exists
    if not os.path.exists(contestant['cwd']):
        print(f"⚠️  Error: Directory {contestant['cwd']} not found. Skipping.")
        return None

    start_time = time.perf_counter()
    
    try:
        # Run the subprocess
        result = subprocess.run(
            contestant['cmd'],
            cwd=contestant['cwd'],
            capture_output=True,
            text=True,
            check=True # Raises error if exit code is non-zero
        )
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        print(f"✅ Finished in {duration:.6f} seconds.")
        # Optional: Print output to verify it actually worked
        # print(f"Output: {result.stdout.strip()}")
        
        return {
            "language": contestant['name'],
            "duration_seconds": duration,
            "status": "Success",
            "timestamp": datetime.datetime.now().isoformat()
        }

    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED: {e.stderr}")
        return {
            "language": contestant['name'],
            "duration_seconds": 0,
            "status": "Failed",
            "error": str(e)
        }
    except FileNotFoundError:
        print(f"❌ FAILED: Command not found. Is the language installed?")
        return {
            "language": contestant['name'],
            "duration_seconds": 0,
            "status": "Missing Toolchain"
        }

def main():
    ensure_directories()
    results = []

    print("🏁 BEGINNING BATTLE ROYALE 🏁")
    print("===============================")

    for contestant in CONTESTANTS:
        data = run_benchmark(contestant)
        if data:
            results.append(data)
        print("-------------------------------")

    # Save to JSON
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\n🏆 Tournament Complete. Findings saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
