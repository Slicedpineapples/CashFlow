# To run the CashFlow system, run this file.
import subprocess
import os
import time

# Paths
BACKEND_DIR = os.path.join(os.getcwd(), 'back')
FRONTEND_DIR = os.path.join(os.getcwd(), 'front')

# Commands
BACKEND_COMMAND = ['python3', 'api.py']
FRONTEND_COMMAND = ['node', 'server.js']

def start_backend():
    print("Starting backend...")
    return subprocess.Popen(BACKEND_COMMAND, cwd=BACKEND_DIR)

def start_frontend():
    print("Starting frontend...")
    return subprocess.Popen(FRONTEND_COMMAND, cwd=FRONTEND_DIR)

if __name__ == "__main__":
    try:
        backend_process = start_backend()
        time.sleep(2)
        frontend_process = start_frontend()

        print("CasFlow is running. Press Ctrl+C to stop.")

        # Keep script alive
        backend_process.wait()
        frontend_process.wait()

    except KeyboardInterrupt:
        print("\nShutting CashFlow servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Stopped.")
