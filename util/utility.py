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

def transfer_to_nb(unit):
    if "pb" in unit:
        return 1.e3
    if "nb" in unit:
        return 1.
    if "\mu" in unit:
        return 1.e-3
    print("warning: unrecognized unit: "+unit)
    return 1

def merge_json_array(source):
    source.sort()
    result = []
    thismin = -1
    thismax = -1
    for s in source:
        if thismin < 0:
            thismin = s
            thismax = s
            continue
        if s == (thismax + 1):
            thismax = s
        else:
            result.append([thismin, thismax])
            thismin = s
            thismax = s
    result.append([thismin, thismax])
    return result
