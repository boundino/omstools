import json
import argparse
import sys

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print HLT counts in given lumi ranges of runs')
    parser.add_argument('--timemin', required = True, help = 'Start date, e.g. 2023-09-19')
    parser.add_argument('--timemax', required = False, help = 'Optional End date, e.g. 2023-09-20')
    # parser.add_argument('--pathnames', required = True, help = 'e.g. HLT_ZeroBias_v8,HLT_PPRefL1SingleMu7_v1')
    parser.add_argument('--outcsv', required = False, help = 'Optional csv output file')
    args = parser.parse_args()

    start_time = args.timemin
    end_time = args.timemax
    
    q = o.omsapi.query("runs")
    q.set_verbose(False)
    q.filter("start_time", start_time, "GE").filter("end_time", end_time, "LE")
    datas = []
    ipage = 1
    while True:
        # print("page: " + str(ipage))
        q.paginate(page = ipage, per_page = 100)
        qjson = q.data().json()
        data = qjson["data"]
        if not data:
            print("\033[31merror: no stable beam: \"\033[4m" + start_time + ", " + end_time + "\033[0m\033[31m\", give up..\033[0m")
            sys.exit()
        datas.extend(data)
        if qjson["links"]["next"] is None:
            break;
        ipage = ipage+1

    print('-' * 179)
    print('|{:>7} | {:>6} |{:>5} |{:>20} |{:>20} |{:>16} |{:>17} |{:>10} |{:>11} |{:>45} |'.format("Run", "Stable", "Fill",
                                                                                               "Start time", "End time",
                                                                                               "Recorded (nb-1)", "Delivered (nb-1)",
                                                                                               "L1 rate", "HLT (GB/s)", "HLT menu"))
    print('-' * 179)
    for d in datas:
        hltkey = d["attributes"]["hlt_key"]
        if not hltkey or not d["attributes"]["hlt_physics_throughput"]:
            continue
        if "PRef" not in hltkey and "HIon" not in hltkey:
            continue

        o.print_run_line(d)

    print('-' * 179)
