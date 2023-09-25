import json
import argparse
import sys

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print HLT summary of a given run')
    parser.add_argument('--run', required = True, help = 'one run number')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()
    
    run = args.run

    rundetails = o.get_run_info(run, verbose = True)
    if not rundetails: sys.exit()
    hltconfig = o.get_hltconfig_info(rundetails["attributes"]["hlt_key"])
    if not hltconfig: sys.exit()

    q = o.omsapi.query("hltpathinfo")
    q.paginate(per_page = 1000)
    q.set_verbose(False)
    q.filter("run_number", run)
    data = q.data().json()["data"]

    outputfile = u.setoutput(args.outcsv, 'outcsv/hltrunsummary.csv')
    results = []
    with open(outputfile, 'w') as f:
        print("HLT Path, L1 seed, Rate (Hz), L1 Pass, PS Pass, Accepted", file = f)
        for d in data:
            attr = d["attributes"]
            # if "HLT_" not in attr["path_name"]:
            #     continue
            config = o.get_item_data(hltconfig, "path_name", attr["path_name"])
            ele = { "path" : attr["path_name"],
                    "l1_prerequisite" : config["attributes"]["l1_prerequisite"],
                    "rate" : str(attr["rate"]),
                    "l1_pass" : str(attr["l1_pass"]),
                    "ps_pass" : str(attr["ps_pass"]),
                    "accepted" : str(attr["accepted"]),
                   }
            for e in ele:
                print(u.mystr(ele[e]) + ", ", end = "", file = f)
            print("", file = f)
            results.append(ele)

    print('-' * 158)
    print('|{:>45} |{:>15} |{:>15} |{:>10} |{:>10} |{:>50} |'.format("HLT Path", "Rate (Hz)", "L1 Pass", "PS Pass", "Accepted", "L1 seed"))
    print('-' * 158)
    for rr in results:
        print('|{:>45} |{:>15} |{:>15} |{:>10} |{:>10} |{:>50} |'.format(u.mystr(rr["path"]), u.mystr(rr["rate"]), u.mystr(rr["l1_pass"]), u.mystr(rr["ps_pass"]), u.mystr(rr["accepted"]), u.mystr(rr["l1_prerequisite"])))
    print('-' * 158)
    print()    
