import sys
import subprocess
def downloadReqs():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'requests'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'altair'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'altair_viewer'])