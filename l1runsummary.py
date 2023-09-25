import json
import argparse
import sys

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print L1 summary of a given run')
    parser.add_argument('--run', required = True, help = 'one run number')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    parser.add_argument('--compress', required = False, help = 'Optional filter turned-on bits', action = "store_true")
    args = parser.parse_args()
    
    run = args.run

    rundetails = o.get_run_info(run, verbose = True)
    if not rundetails: sys.exit()
    hltconfig = o.get_hltconfig_info(rundetails["attributes"]["hlt_key"])
    if not hltconfig: sys.exit()

    q = o.omsapi.query("l1algorithmtriggers")
    q.paginate(per_page = 1000)
    q.set_verbose(False)
    q.custom("group[granularity]", "run")
    q.filter("run_number", run)
    data = q.data().json()["data"]

    outputfile = u.setoutput(args.outcsv, 'outcsv/l1runsummary.csv')
    results = []
    maxlen = 0
    with open(outputfile, 'w') as f:
        print("L1 bit, Name, Pre-DT before PS (Hz), Pre-DT after PS (Hz), Post-DT (Hz), Post-DT from HLT (Hz)", file = f)
        for d in data:
            attr = d["attributes"]
            ele = { "bit" : attr["bit"],
                    "name" : attr["name"],
                    "pre_dt_before_prescale_rate" : attr["pre_dt_before_prescale_rate"],
                    "pre_dt_rate" : attr["pre_dt_rate"],
                    "post_dt_rate" : attr["post_dt_rate"],
                    "post_dt_hlt_rate" : attr["post_dt_hlt_rate"],
                   }
            if len(ele["name"]) > maxlen: maxlen = len(ele["name"])
            for e in ele:
                print(u.mystr(ele[e], 0) + ", ", end = "", file = f)
            print("", file = f)
            results.append(ele)

    nl = 67 + maxlen
    print('-' * nl)
    print('| {:>4} | {:<{width}} |{:>13} |{:>12} |{:>10} |{:>13} |'.format("", "", "Pre-DT [Hz]", "Pre-DT [Hz]", "Post-DT", "Post-DT [Hz]", width = maxlen))
    print('| {:>4} | {:<{width}} |{:>13} |{:>12} |{:>10} |{:>13} |'.format("Bit", "Name", "before PS", "after PS", "[Hz]", "from HLT", width = maxlen))
    print('-' * nl)
    for rr in results:
        if args.compress and not rr["pre_dt_rate"]:
            continue
        print('| {:>4} | {:<{width}} |{:>13} |{:>12} |{:>10} |{:>13} |'.format(u.mystr(rr["bit"]), u.mystr(rr["name"]),
                                                                              u.mystr(round(rr["pre_dt_before_prescale_rate"], 2), 0),
                                                                              u.mystr(round(rr["pre_dt_rate"], 2), 0),
                                                                              u.mystr(round(rr["post_dt_rate"], 2), 0),
                                                                              u.mystr(round(rr["post_dt_hlt_rate"], 2), 0),
                                                                              width = maxlen));
    print('-' * nl)
    print()    
