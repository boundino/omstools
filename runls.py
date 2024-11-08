import json
import argparse
import sys

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print lumi sections of a given run')
    parser.add_argument('--run', required = True, help = 'one run number')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()
    
    run = args.run

    rundetails = o.get_run_info(run, verbose = True)
    lumisections = o.get_by_range("run_number", run, run, "lumisections")
    
    outputfile = u.setoutput(args.outcsv, 'outcsv/runls.csv')
    results = []
    maxlen = 0
    with open(outputfile, 'w') as f:
        print("LS, beams_stable, init_lumi, L1 Pass, PS Pass, Accepted", file = f)
        for d in lumisections:
            attr = d["attributes"]
            ele = { "lumisection_number" : attr["lumisection_number"],
                    "beams_stable" : attr["beams_stable"],
                    "start_time" : attr["start_time"],
                    "end_time" : attr["end_time"],
                    "init_lumi" : attr["init_lumi"],
                    "end_lumi" : attr["end_lumi"],
                    "prescale_name" : u.mystr(attr["prescale_name"]),
                    "recorded_lumi" : attr["recorded_lumi"],
                    "delivered_lumi" : attr["delivered_lumi"],
                   }
            if len(ele["prescale_name"]) > maxlen: maxlen = len(ele["prescale_name"])
            for e in ele:
                print(u.mystr(ele[e]) + ", ", end = "", file = f)
            print("", file = f)
            results.append(ele)

    nl = (7 + +9 + 19 + 15 + 4) + maxlen
    print('-' * nl)
    print('| {:>4} | {:>6} | {:>16} | {:>12} | {:<{width}} |'.format("", "", "Avg. lumi", "Record. lumi", "", width = maxlen))
    print('| {:>4} | {:>6} | {:>16} | {:>12} | {:<{width}} |'.format("LS", "Stable", "10^33 cm^-2 s^-1", "mub-1", "Precale", width = maxlen))
    print('-' * nl)
    for rr in results:
        tstable = u.mystr(rr["beams_stable"])
        color = 0
        if rr["beams_stable"] == None:
            tstable = ""
        elif rr["beams_stable"]:
            tstable = "True"
            color = "32"
        else:
            tstable = "False"
            color = "31"
        tstable = '\033[{}m{:<6}\033[0m'.format(color, tstable)
        print('| {:>4} | {:<6} | {:>16} | {:>12} | {:<{width}} |'.format(u.mystr(rr["lumisection_number"]), tstable, u.mystr((rr["init_lumi"]+rr["end_lumi"]) / 2., ndigi = 3, scien = True), u.mystr(rr["recorded_lumi"], ndigi = 3, scien = True), u.mystr(rr["prescale_name"]), width = maxlen))
    print('-' * nl)
    print()    
