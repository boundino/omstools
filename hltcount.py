import json
import argparse

from util.oms import omsapi
import util.utility as u

def getcount(runlumijson, path, omsapi = omsapi):
    q = omsapi.query("hltpathrates")
    q.paginate(per_page = 3000)
    q.set_verbose(False)
    totalcount = 0
    for run in runlumijson:
        q.clear_filter()
        q.filter("path_name", path).filter("run_number", run)
        if not q.data().json()["data"]:
            print("\033[31merror: bad path name or run number: \"\033[4m" + path + ", " + run + "\033[0m\033[31m\", skip it..\033[0m")
            continue

        for ls in runlumijson[run]:
            lumimin = ls[0]
            lumimax = ls[1]
        
            if lumimin >= 0:
                q.filter("first_lumisection_number", lumimin, "GE")
            if lumimax >= 0:
                q.filter("last_lumisection_number", lumimax, "LE")

            datajson = q.data().json()
            for ls in datajson["data"]:
                totalcount += ls["attributes"]["counter"]

    return totalcount

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print HLT counts in given lumi ranges of runs')
    parser.add_argument('--lumiranges', required = True, help = '<run>(:<minLS>:<maxLS>) e.g. 373664:25:30,373710 || (option 2) cert json file')
    parser.add_argument('--pathnames', required = True, help = 'e.g. HLT_ZeroBias_v8,HLT_PPRefL1SingleMu7_v1')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()
    
    pathsStr = args.pathnames.split(",")
    outputfile = u.setoutput(args.outcsv, "outcsv/hltcount.csv")

    lumiRangesStr = args.lumiranges.split(",")
    runlumi = {}
    if len(lumiRangesStr) == 1 and lumiRangesStr[0].endswith(".json") :
        with open(lumiRangesStr[0]) as ff:
            runlumi = json.load(ff)
    else:
        if len(lumiRangesStr) == 1 and lumiRangesStr[0].endswith(".txt") :
            text_file = open(lumiRangesStr[0], "r")
            lines = text_file.read().splitlines()
            lumiRangesStr = lines
        for str in lumiRangesStr:
            lumistr = str.split(":")
            thisrun = lumistr[0]
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

            if thisrun not in runlumi:
                newele = [thismin, thismax]
                runlumi[thisrun] = []
                runlumi[thisrun].append(newele)
            else:
                treat = 0
                for ls in runlumi[thisrun]:
                    if (thismin <= ls[0] or thismin < 0) and (thismax >= ls[0]):
                        ls[0] = thismin
                        treat = 1
                    if (thismax >= ls[1] or thismax < 0) and (thismin <= ls[1]):
                        ls[1] = thismax
                        treat = 1
                if treat == 0:
                    newele = [thismin, thismax]
                    runlumi[thisrun].append(newele)

    print("Summing up lumi sections: \033[4;32;1m", end = "")
    print(runlumi, end = "")
    print("\033[0m")
    
    counts = {}
    with open(outputfile, 'w') as f:
        print("HLT Path, Counts", file = f)
        for p in pathsStr:
            totalcount = getcount(runlumi, p)
            print(p + ", " + f'{totalcount}', file = f)
            counts[p] = totalcount

    print('-' * 60)
    print('|{:>40} |{:>15} |'.format("HLT Path", "Count"))
    print('-' * 60)
    for p in counts:
        print('|{:>40} |{:>15} |'.format(p, counts[p]))
    print('-' * 60)
    print()
