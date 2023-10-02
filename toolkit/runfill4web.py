import json
import argparse
import sys

from datetime import datetime

import util.oms as o
import util.utility as u

def translate(datas, keys = [], category = "runs"):
    results = {}
    for d in datas:
        if "run" in category:
            hltkey = d["attributes"]["hlt_key"]
            if not hltkey or not d["attributes"]["hlt_physics_throughput"]:
                continue
            if "PRef" not in hltkey and "HI" not in hltkey:
                continue
            if not d["attributes"]["recorded_lumi"]:
                continue
            if d["attributes"]["recorded_lumi"] <= 0:
                continue
        r = {}
        for k in keys:
            r[k] = d["attributes"][k]
        results[d["id"]] = r
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Save js for web')
    parser.add_argument('--timemin', required = True, help = 'Start date, e.g. 2023-09-19T18:00:00')
    parser.add_argument('--timemax', required = False, help = 'Optional End date, e.g. 2023-09-20')
    args = parser.parse_args()

    start_time = args.timemin
    if args.timemax:
        end_time = args.timemax
    else:
        # end_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        end_time = None
        
    runs = o.get_runs_by_time(start_time, end_time)
    r_runs = translate(runs, ["duration",
                              "hlt_physics_throughput",
                              "recorded_lumi",
                              "delivered_lumi",
                              "fill_number",
                              "end_time",
                              "start_time",
                              "hlt_key",
                              "last_lumisection_number",
                              "l1_rate",
                              "l1_menu",
                              "cmssw_version",
                              "stable_beam",
                              "components_out"], "runs")
    
    with open('../cms-hin-coordination/webs/public/run/js/runs.js', 'w') as f:
        print('let runinfo = ', file = f)
        json.dump(r_runs, f, indent = 2)

    fillarray = []
    for r in r_runs:
        if r_runs[r]["fill_number"] not in fillarray:
            fillarray.append(r_runs[r]["fill_number"])

    fills = o.get_by_array("fill_number", fillarray, category = "filldetails")
    r_fills = translate(fills, ["injection_scheme",
                                "fill_type_party2",
                                "fill_type_party1",
                                "bunches_colliding",
                                ], "fills")

    with open('../cms-hin-coordination/webs/public/run/js/fills.js', 'w') as f:
        print('let fillinfo = ', file = f)
        json.dump(r_fills, f, indent = 2)
