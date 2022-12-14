import sys
import subprocess
import importlib.util

def downloadReqs():
    for i in ["requests", "scipy"]:
        spec = importlib.util.find_spec(i)
        if spec is None:
            print(i +" is not installed, will install the package for you")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
            i])
        else: print(i + " found")