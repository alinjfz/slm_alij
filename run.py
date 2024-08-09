import subprocess
import os

def run_flask():
    os.system('python slm_back/server.py')

def run_react():
    subprocess.Popen(['npm', 'start'], cwd='slm_front')

def run_llama():
    subprocess.Popen(['ollama', 'run', 'llama3.1:8b'])

if __name__ == '__main__':
    run_llama()
    run_react()
    run_flask()
