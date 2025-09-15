import os
import subprocess
import sys

def run_scripts(script_path):
    try:
        print(f"[INFO] Starting {script_path} ...")
        subprocess.run([sys.executable, script_path], check=True)  # use same Python env
        print(f"[SUCCESS] Finished {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to run {script_path}.")
        print("[DETAILS]", e)

if __name__ == "__main__":

    # BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    # print("base path: " + BASE_PATH)
    # ROOT_PATH = os.path.dirname(BASE_PATH)
    # print("root path: " + ROOT_PATH)

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    # print("Script directory:", BASE_PATH)

    print("=== Starting Pipeline ===")


    # run_scripts(os.path.join(BASE_PATH, "scripts", "rect_selector.py"))
    run_scripts(os.path.join(BASE_PATH, "scripts", "split_by_black_region.py"))
    run_scripts(os.path.join(BASE_PATH, "scripts", "generate_report.py"))
    
    print("Running Completed")
