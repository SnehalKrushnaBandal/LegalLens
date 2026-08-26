import subprocess
import sys
import os
import time

def main():
    print("=" * 70)
    print("  LEGAL METROLOGY COMPLIANCE ENFORCEMENT SYSTEM (SIH 2026 - SIH26034)  ")
    print("=" * 70)
    print("Starting FastAPI Backend & React Frontend...\n")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")

    # 1. Start Backend
    print("[1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=backend_dir
    )

    time.sleep(2)

    # 2. Start Frontend
    print("[2/2] Launching Vite Frontend on http://localhost:5173 ...")
    frontend_cmd = "npm run dev"
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=root_dir,
        shell=True
    )

    print("\n" + "=" * 70)
    print("  SYSTEM IS LIVE!")
    print("  Frontend URL : http://localhost:5173")
    print("  Backend API  : http://127.0.0.1:8000")
    print("  API Docs     : http://127.0.0.1:8000/docs")
    print("  Demo Officer : LMO001 / admin123")
    print("=" * 70)
    print("Press Ctrl+C to stop all servers.\n")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
