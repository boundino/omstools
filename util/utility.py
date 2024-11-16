import os
import copy
import json

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
    elif "mu" in unit:
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

# https://github.com/cms-sw/cmssw/blob/master/FWCore/PythonUtilities/python/LumiList.py#L182
def lumimask_or(ajson, bjson):
    result = {}
    aruns = list(ajson.keys())
    bruns = list(bjson.keys())
    runs = set(aruns + bruns)
    for run in runs:
        overlap = sorted(ajson.get(run, []) + bjson.get(run, []))
        unique = [copy.deepcopy(overlap[0])]
        for pair in overlap[1:]:
            if pair[0] >= unique[-1][0] and pair[0] <= unique[-1][1]+1 and pair[1] > unique[-1][1]:
                unique[-1][1] = copy.deepcopy(pair[1])
            elif pair[0] > unique[-1][1]:
                unique.append(copy.deepcopy(pair))
        result[run] = unique
    result = dict(sorted(result.items()))
    return result


def mystr(item, fill = "null", ndigi = -1, scien = False):
    result = str(item)
    if item:
        if ndigi >= 0 and scien:
            result = '{:.{dec}e}'.format(item, dec = ndigi)
    else:
        result = str(fill)    
    return result

def prop_to_list(adict, prop):
    result = []
    for a in adict:
        result.append(a[prop])
    return result


def progressbars():
    print(u'\033[36m\u25ac\033[0m', end = "", flush = True)
def progressrange(i, total):
    print(u' \033[36m{i}/{total} done.\033[0m'.format(i=i, total=total), end = "\r", flush = True)    
def progressbars_summary(npage):
    print(' \033[36m{n}/{n} done.\033[0m'.format(n = npage))
