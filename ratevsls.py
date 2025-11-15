import json
import argparse
import sys
import os
import matplotlib.pyplot as plt

import util.oms as o
import util.utility as u

stable_only = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'HLT or L1 rates vs lumi sections for selected runs')
    parser.add_argument('--runs', required = True, help = 'run number list')
    parser.add_argument('--pathname', required = True, help = 'HLT path or L1 seed')
    parser.add_argument('--l1postdt', required = False, help = 'Optional store L1 post DT rate instead of pre PS rate', action = "store_true")
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    parser.add_argument('--unstable', required = False, action='store_true', help = 'Include unstable runs and LSs')
    args = parser.parse_args()
    
    inputruns = args.runs.split(',')
    pathname = args.pathname

    runs = []
    color = [ "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",
              "tab:pink", "tab:brown", "tab:gray", "tab:olive", "tab:cyan",
              "tab:yellow", "tab:bluegreen", "tab:orangebrown", "tab:greenyellow", "tab:redorange",
              "tab:purpleblue", "tab:pinkred", "tab:graybrown", "tab:greenyellow", "tab:lightblue" ]
    color_runs = []
    for str_run in inputruns:
        parts = str_run.split(":")
        runs.append(parts[0])
        if len(parts) > 1:
            cc = "tab:" + parts[1]
            if cc in color:
                color.remove(cc)
        else:
            cc = color.pop(0) if color else "black"

        color_runs.append(cc)
    
    print("L1 rate option: \033[4m", end = "")
    key_l1 = "pre_dt_before_prescale_rate"
    if args.l1postdt:
        key_l1 = "post_dt_rate"

    print(key_l1+"\033[0m")

    if args.unstable:
        stable_only = False

    if pathname.startswith("L1_"):
        trigtype = "l1"
        rate_var = key_l1
    elif pathname.startswith("HLT_"):
        trigtype = "hlt"
        rate_var = "rate"
    if not trigtype:
        print("error: pathname is not L1_ or HLT_")
        quit()
    
    results = {}

    for run in runs:
        rundetails = o.get_run_info(run, verbose = True)
        print("\033[2mGetting stable lumisections...\033[0m")
        lumisections = o.get_by_range("run_number", run, run, "lumisections", per_page = 100, onlystable = stable_only)
        print("\033[2mGetting rate...\033[0m")
        rates = o.get_rate_by_runls(run, 0, category = trigtype, path = pathname)
    
        results[run] = []
        for d in lumisections:
            attr = d["attributes"]
            if (stable_only and attr["beams_stable"] == False) or not attr["prescale_name"]: continue
            ele = { "lumisection_number" : attr["lumisection_number"],
                    "beams_stable" : attr["beams_stable"],
                    "start_time" : attr["start_time"],
                    "end_time" : attr["end_time"],
                    "init_lumi" : attr["init_lumi"],
                    "end_lumi" : attr["end_lumi"],
                    "prescale_name" : u.mystr(attr["prescale_name"]),
                    "recorded_lumi" : attr["recorded_lumi"],
                    "delivered_lumi" : attr["delivered_lumi"],
                    "rate" : None,
                   }
            for rr in rates:
                if rr["attributes"]["last_lumisection_number"] == ele["lumisection_number"]:
                    if rate_var in rr["attributes"]:
                        ele["rate"] = rr["attributes"][rate_var]
                    break
            if not ele["rate"]: continue
            results[run].append(ele)
            
    outputfile = u.setoutput(args.outcsv, 'outcsv/ratevsls_'+pathname+'.csv')
    with open(outputfile, 'w') as f:
        for t in results[runs[0]][0]:
            print(t + ", ", file = f, end = "")
        print(file = f)

        for run in runs:
            print(u.mystr(run) + ", ", file = f)
            for ele in results[run]:
                for e in ele:
                    print(u.mystr(ele[e]) + ", ", file = f, end = "")
                print(file = f)

    plt.figure(figsize=(6, 6))
    i = 0
    for run in results:
        x = []
        y = []
        for ls in results[run]:
            x.append(ls["init_lumi"])
            y.append(ls["rate"])
        plt.scatter(x, y, s=20, c=color_runs[i], alpha=0.5, label=u.mystr(run))
        i = i+1

    plt.xlabel(r"Inst luminosity [10$^{33}$ cm$^{-2}$ s$^{-1}$]")
    plt.ylabel("Rate")
    plt.title(pathname)
    plt.legend(frameon = False, loc = 'best', bbox_to_anchor = (0.26, 0.98))

    plt.xlim(left=0)  # Set minimum value of x-axis to 0
    plt.ylim(bottom=0)  # Set minimum value of y-axis to 0

    os.system('mkdir -p figs')
    plt.savefig('figs/ratevsls_'+pathname+'.png', format="png", dpi=200, bbox_inches="tight")
    print('open \033[4mfigs/ratevsls_'+pathname+'.png\033[0m')
    os.system('open figs/ratevsls_'+pathname+'.png')
