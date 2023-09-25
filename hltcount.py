import json
import argparse

from util.oms import omsapi
import util.utility as u
import util.oms as o

def getcount(runlumijson, path, omsapi = o.omsapi):
    q = omsapi.query("hltpathrates")
    q.paginate(per_page = 3000)
    q.set_verbose(False)
    totalcount = 0
    for run in runlumijson:
        q.clear_filter()
        q.filter("path_name", path).filter("run_number", run)
        if not q.data().json()["data"]:
            print("\033[31mwarning: bad path name or run number: \"\033[4m" + path + ", " + run + "\033[0m\033[31m\", skip it..\033[0m")
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
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--lumiranges', help = '(option 1) <run>(:<minLS>:<maxLS>) e.g. 373664:25:30,373710 || (option 2) cert json file')
    group.add_argument('--timerange', help = '(option 3) <start_time>,<end_time>')
    parser.add_argument('--pathnames', required = True, help = 'List of HLT paths, (option 1) HLT_1,HLT_2,HLT_3 (option 2) .txt file with each line as an HLT path')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()

    outputfile = u.setoutput(args.outcsv, "outcsv/hltcount.csv")

    runlumi = {}
    if args.lumiranges:
        lumiRangesStr = args.lumiranges.split(",")
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
                if len(lumistr) != 1 and len(lumistr) != 3:
                    continue
                thisrun = lumistr[0]
                if len(lumistr) == 1:
                    lumistr.extend(['-1', '-1'])
                thismin = int(lumistr[1])
                thismax = int(lumistr[2])
                if thismin > thismax: 
                    print("\033[31merror: bad lumi range: \"\033[4m" + str + "\033[0m\033[31m\", skip it..\033[0m")
                    continue

                if thisrun not in runlumi:
                    runlumi[thisrun] = []
                    runlumi[thisrun].append([thismin, thismax])
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
                        runlumi[thisrun].append([thismin, thismax])

    if args.timerange:
        timebs = args.timerange.split(",")
        if len(timebs) == 2:
            datas = o.get_runs_by_time(timebs[0], timebs[1], "lumisections")
            # print(datas)
            runlumi = o.get_json_by_lumi(datas)

    print("Summing up lumi sections: \033[4;32;1m", end = "")
    print(runlumi, end = "")
    print("\033[0m")

    pathnames = []
    if args.pathnames:
        pathnames = args.pathnames.split(",")
        if len(pathnames) == 1 and pathnames[0].endswith(".txt"):
            text_file = open(pathnames[0], "r")
            pathnames = text_file.read().splitlines()
    elif list(runlumi.keys()):
        pathnames = o.get_hltlist_by_run(list(runlumi.keys())[0])
    
    counts = {}
    maxlen = 0
    with open(outputfile, 'w') as f:
        print("HLT Path, Counts", file = f)
        for p in pathnames:
            totalcount = getcount(runlumi, p)
            print(p + ", " + f'{totalcount}', file = f)
            counts[p] = totalcount
            if len(p) > maxlen: maxlen = len(p)

    nl = 21 + maxlen
    print('-' * nl)
    print('| {:<{width}} |{:>15} |'.format("HLT Path", "Count", width = maxlen))
    print('-' * nl)
    for p in counts:
        print('| {:<{width}} |{:>15} |'.format(p, counts[p], width = maxlen))
    print('-' * nl)
    print()
