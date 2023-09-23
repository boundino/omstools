import json
import argparse

from util.oms import omsapi

def getcount(runlumijson, path, omsapi = omsapi):
    q = omsapi.query("hltpathrates")
    q.paginate(per_page = 1000)
    q.set_verbose(False)
    totalcount = 0
    for run in runlumijson:
        q.clear_filter()
        q.filter("path_name", path).filter("run_number", run)
        if not q.data().json()["data"]:
            print("\033[31merror: bad path name or run number: \"\033[4m" + path + ", " + run + "\033[0m\033[31m\", skip it..\033[0m")
            continue

        lumimin = runlumijson[run]["min"]
        lumimax = runlumijson[run]["max"]
        
        if lumimin >= 0:
            q.filter("first_lumisection_number", lumimin, "GE")
        if lumimax >= 0:
            q.filter("last_lumisection_number", lumimax, "LE")

        datajson = q.data().json()
        for ls in datajson["data"]:
            # print(ls["attributes"]["first_lumisection_number"])
            totalcount += ls["attributes"]["counter"]

    return totalcount

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print HLT counts in given lumi ranges of runs')
    parser.add_argument('--lumiranges', required = True, help = 'e.g. 373664:25:30,373710 => <run>(:<minLS>:<maxLS>)')
    parser.add_argument('--pathnames', required = True, help = 'e.g. HLT_ZeroBias_v8,HLT_PPRefL1SingleMu7_v1')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()
    
    pathsStr = args.pathnames.split(",")
    outputfile = 'outcsv/hltcount.csv'
    if args.outcsv != None:
        outputfile = args.outcsv
    print("Write to output file: " + outputfile)

    lumiRangesStr = args.lumiranges.split(",")
    runlumi = {}
    if len(lumiRangesStr) == 1 and lumiRangesStr[0].endswith(".txt") :
        text_file = open(lumiRangesStr[0], "r")
        lines = text_file.read().splitlines()
        lumiRangesStr = lines
    for str in lumiRangesStr:
        lumistr = str.split(":")
        if len(lumistr) == 1:
            lumistr.extend(['-1', '-1'])
        elif len(lumistr) != 3:
            print("\033[31merror: bad lumi range: \"\033[4m" + str + "\033[0m\033[31m\", skip it..\033[0m")
            continue
        thismin = int(lumistr[1])
        thismax = int(lumistr[2])
        if thismin > thismax: 
            print("\033[31merror: bad lumi range: \"\033[4m" + str + "\033[0m\033[31m\", skip it..\033[0m")
            continue

        if lumistr[0] not in runlumi:
            newele = {"min" : thismin, "max" : thismax}
            runlumi[lumistr[0]] = newele
        else:
            if thismin < runlumi[lumistr[0]]["min"] or thismin < 0:
                runlumi[lumistr[0]]["min"] = thismin
            if (thismax > runlumi[lumistr[0]]["max"] and runlumi[lumistr[0]]["max"] >= 0) or thismax < 0:
                runlumi[lumistr[0]]["max"] = thismax

    print("Processing lumi sections: ", end="")
    print(runlumi)
    print()
    with open(outputfile, 'w') as f:
        print("HLT Path, Counts", file = f)
        for p in pathsStr:
            totalcount = getcount(runlumi, p)
            print(p + ", " + f'{totalcount}', file = f)
            print('{:>30} {:>10}'.format(p, totalcount))
    print()
