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

def translate_lumi_unit(unit, tounit):
    sf = 0.
    # default: mub
    if "pb" in unit:
        sf = 1.e6
    elif "nb" in unit:
        sf = 1.e3
    elif "\mu" in unit:
        sf = 1.

    if "nb" in tounit:
        sf = sf * 1.e-3
    elif "pb" in tounit:
        sf = sf * 1.e-6

    if sf == 0:
        print("warning: unrecognized unit (tounit): " + unit + " ("+tounit+")")
    return sf

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

def mystr(item):
    if item:
        return str(item)
    return "null"
