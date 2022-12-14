import sys
import subprocess
def downloadReqs():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'requests'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'scipy'])

    
if __name__=="__main__":
    downloadReqs()
    print("help me")