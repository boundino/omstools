import json
import argparse
import sys

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'HLT paths or L1 rates or counts for a given set of runs/lumi sections')
    parser.add_argument('--runls', required = True, help = 'List of run with optional lumi section, e.g. 373710,373710:740')
    parser.add_argument('--pathnames', required = True, help = 'List of HLT paths or L1 seeds, (option 1) HLT_1,L1_1,L1_2 (option 2) .txt file with each line as an HLT/L1')
    parser.add_argument('--l1preps', required = False, help = 'Optional store L1 pre PS rate instead of post DT rate', action = "store_true")
    parser.add_argument('--count', required = False, help = 'Optional store count instead of rate', action = "store_true")
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()
    
    runs = args.runls.split(",")
    pathnames = args.pathnames.split(",")
    if len(pathnames) == 1 and pathnames[0].endswith(".txt"):
        text_file = open(pathnames[0], "r")
        lines = text_file.read().splitlines()
        pathnames = lines
    
    print("Variable option: \033[4m", end = "")
    key_var = "rate" ; rd = 3
    if args.count:
        key_var = "counter"
        rd = 0
        print("count", end = "")
    else:
        print("rate", end = "")
    print("\033[0m")

    print("L1 rate option: \033[4m", end = "")
    key_l1 = "post_dt_" + key_var
    if args.l1preps:
        key_l1 = "pre_dt_before_prescale_" + key_var
        print("Pre-DT before PS", end = "")
    else:
        print("Post-DT after PS", end = "")
    print("\033[0m")
        

    rate_results={};
    maxlen = 0
    for p in pathnames:
        rate_results[p] = {}
        if len(p) > maxlen: maxlen = len(p)
        
    for run in runs:
        rls = run.split(":")
        hlts = []
        l1s = []
        if len(rls) == 1:
            l1s = o.get_rate_by_runls(rls[0], category = "l1")
            hlts = o.get_rate_by_runls(rls[0], category = "hlt")
        elif len(rls) == 2:
            l1s = o.get_rate_by_runls(rls[0], rls[1], "l1")
            hlts = o.get_rate_by_runls(rls[0], rls[1], "hlt")
            
        for path in pathnames:
            rate_results[path][run] = -1

        for l1 in l1s:
            name = l1["attributes"]["name"]
            if name in pathnames:
                rate_results[name][run] = l1["attributes"][key_l1]
                
        for hlt in hlts:
            name = hlt["attributes"]["path_name"]
            if name in pathnames:
                if key_var in hlt["attributes"]:
                    rate_results[name][run] = hlt["attributes"][key_var]
                else:
                    rate_results[name][run] = hlt["attributes"]["accepted"]

    outputfile = u.setoutput(args.outcsv, 'outcsv/ratetable.csv')
    with open(outputfile, 'w') as f:
        print("Path", file = f, end = "")
        for run in runs:
            print(", " + u.mystr(run), file = f, end = "")
        print(file = f)
        for p in pathnames:
            print(p, file = f, end = "")
            for run in runs:
                print(", " + u.mystr(rate_results[p][run], 0), file = f, end = "")
            print(file = f)

    nl = 4 + 14*len(runs) + maxlen
    if key_var == "rate": print(" "*(nl-4) + "[Hz]")
    print('-' * nl)
    print('| {:<{width}} '.format("Path / L1 seed", width = maxlen), end = "")
    for run in runs:
        print('|{:>12} '.format(run), end = "")
    print("|")
    print('-' * nl)
    for p in pathnames:
        print('| {:<{width}} '.format(p, width = maxlen), end = "")
        for run in runs:
            print('|{:>12} '.format(round(rate_results[p][run], rd)), end = "")
        print("|")
    print('-' * nl)

