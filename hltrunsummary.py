import json
import argparse
import sys

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print HLT summary of a given run')
    parser.add_argument('--run', required = True, help = 'one run number')
    parser.add_argument('--pathnames', required = False, help = 'Optional HLT paths')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()
    
    run = args.run

    rundetails = o.get_run_info(run, verbose = True)
    if not rundetails: sys.exit()
    hltconfig = o.get_hltconfig_info(rundetails["attributes"]["hlt_key"])
    if not hltconfig: sys.exit()

    if args.pathnames is None: sys.exit()

    pathsStr = args.pathnames.split(",")
    
    q = o.omsapi.query("hltpathinfo")
    q.paginate(per_page = 1000)
    q.set_verbose(False)

    outputfile = u.setoutput(args.outcsv, 'outcsv/hltrunsummary.csv')
    results = []
    with open(outputfile, 'w') as f:
        print("HLT Path, L1 seed, Rate (Hz), L1 Pass, PS Pass, Accepted", file = f)
        for path in pathsStr:
            q.clear_filter()
            q.filter("path_name", path).filter("run_number", run)
            data = q.data().json()["data"]
            if not data:
                print("\033[31merror: bad path name or run number: \"\033[4m" + path + ", " + run + "\033[0m\033[31m\", skip it..\033[0m")
                continue
            config = o.get_item_data(hltconfig, "path_name", path)
            ele = {"path" : path,
                   "l1_prerequisite" : config["attributes"]["l1_prerequisite"],
                   "rate" : str(data[0]["attributes"]["rate"]),
                   "l1_pass" : str(data[0]["attributes"]["l1_pass"]),
                   "ps_pass" : str(data[0]["attributes"]["ps_pass"]),
                   "accepted" : str(data[0]["attributes"]["accepted"]),
                   }
            for e in ele:
                print(ele[e] + ", ", end = "", file = f)
            print("", file = f)
            results.append(ele)

    print('-' * (130+13))
    print('|{:>40} |{:>40} |{:>15} |{:>15} |{:>10} |{:>10} |'.format("HLT Path", "L1 seed", "Rate (Hz)", "L1 Pass", "PS Pass", "Accepted"))
    print('-' * (130+13))
    for rr in results:
        print('|{:>40} |{:>40} |{:>15} |{:>15} |{:>10} |{:>10} |'.format(rr["path"], rr["l1_prerequisite"], rr["rate"], rr["l1_pass"], rr["ps_pass"], rr["accepted"]))
    print('-' * (130+13))
    print()    
