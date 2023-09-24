import os

def mkdir(outputfile):
    dirname = os.path.dirname(outputfile)
    os.makedirs(dirname, exist_ok = True)

def setoutput(argout, default):
    outputfile = default;
    if argout is not None:
        outputfile = argout
    mkdir(outputfile)
    print("\nWrite to output file: \033[37;4m" + outputfile + "\033[0m")
    return outputfile
