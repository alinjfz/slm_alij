import subprocess
import os

def run_flask():
    os.system('python slm_back/server.py')

def run_react():
    subprocess.Popen(['npm', 'start'], cwd='slm_front')

if __name__ == '__main__':
    run_react()
    run_flask()
