
import shutil

def deleteUnnecessaryFiles():
        try:
            shutil.rmtree('./Src/__pycache__')
            shutil.rmtree('./__pycache__')
        except:
              pass