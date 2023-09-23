import os

def mkdir(outputfile):
    dirname = os.path.dirname(outputfile)
    os.makedirs(dirname, exist_ok = True)
