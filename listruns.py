import json
import argparse
import sys

from datetime import datetime

import util.oms as o
import util.utility as u

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Print runs of interest in a given time range')
    parser.add_argument('--timemin', required = True, help = 'Start date, e.g. 2023-09-19T18:00:00')
    parser.add_argument('--timemax', required = False, help = 'Optional End date, e.g. 2023-09-20')
    parser.add_argument('--stable', required = False, help = 'Optional requiring stable beam runs', action = "store_true")
    parser.add_argument('--unit', required = False, choices = ['mub', 'nb', 'pb'], help = 'Optional lumi unit')
    args = parser.parse_args()

    start_time = args.timemin
    end_time = args.timemax
    datas = o.get_runs_by_time(start_time, end_time)

    unit = "mub"
    if args.unit: unit = args.unit
    
    o.print_run_title(unit = unit)
    for d in datas:
        # print(d)
        hltkey = d["attributes"]["hlt_key"]
        if not hltkey or not d["attributes"]["hlt_physics_throughput"]:
            continue
        if "PRef" not in hltkey and "HI" not in hltkey:
            continue
        if d["attributes"]["delivered_lumi"] <= 0:
            continue
        if not d["attributes"]["stable_beam"] and args.stable:
            continue

        o.print_run_line(d, unit)

    o.print_run_title(onlyline = True)
