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
            # hltkey = d["attributes"]["hlt_key"]
            # if not hltkey or not d["attributes"]["hlt_physics_throughput"]:
            #     continue
            # if "PRef" not in hltkey and "HI" not in hltkey:
            #     continue
            trigger_mode = d["attributes"]["trigger_mode"]
            if not trigger_mode or ("ppref_" not in trigger_mode and "_hi" not in trigger_mode):
                continue
            if not d["attributes"]["recorded_lumi"] or d["attributes"]["recorded_lumi"] <= 0:
                continue
            if not d["attributes"]["l1_rate"] or d["attributes"]["l1_rate"] <= 0:
                continue
            if not d["attributes"]["hlt_physics_throughput"] or d["attributes"]["hlt_physics_throughput"] <= 0:
                continue

        r = {}
        for k in keys:
            r[k] = d["attributes"][k]
        results[d["id"]] = r
    return results

def filljs(runs, outdir):
    r_runs = translate(runs, ["duration",
                              "hlt_physics_throughput",
                              "recorded_lumi",
                              "delivered_lumi",
                              "fill_number",
                              "end_time",
                              "start_time",
                              "trigger_mode",
                              "hlt_key",
                              "last_lumisection_number",
                              "l1_rate",
                              "l1_menu",
                              "cmssw_version",
                              "stable_beam",
                              "l1_key",
                              "components_out"], "runs")
    print("runs done.")
    with open(outdir + 'runs.js', 'w') as f:
        print('let runinfo = ', file = f)
        json.dump(r_runs, f, indent = 2)

    fillarray = []
    for r in r_runs:
        if r_runs[r]["fill_number"] not in fillarray:
            fillarray.append(r_runs[r]["fill_number"])

    fills = o.get_by_array("fill_number", fillarray, category = "filldetailx")
    r_fills = translate(fills, ["injection_scheme",
                                "fill_type_party2",
                                "fill_type_party1",
                                "bunches_colliding",
                                ], "fills")
    print("fills done.")
    with open(outdir + 'fills.js', 'w') as f:
        print('let fillinfo = ', file = f)
        json.dump(r_fills, f, indent = 2)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description = 'Save js for web')
    # parser.add_argument('--timemin', required = True, help = 'Start date, e.g. 2023-09-19T18:00:00')
    # parser.add_argument('--timemax', required = False, help = 'Optional End date, e.g. 2023-09-20')
    # args = parser.parse_args()

    # start_time = args.timemin
    # if args.timemax:
    #     end_time = args.timemax
    # else:
    #     # end_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    #     end_time = None
        
    # runs = o.get_runs_by_time(start_time, end_time)

    # runs_ppref = o.get_by_range(var = "era", lmin = "Run2024J", lmax = "Run2024J", category = "runs", per_page = 100)
    # filljs(runs_ppref, '../cms-hin-coordination/webs/public/run2024/ppref/js/')
    runs_PbPb = o.get_by_range(var = "era", lmin = "HIRun2024A", lmax = "HIRun2024A", category = "runs", per_page = 100)
    filljs(runs_PbPb, '../cms-hin-coordination/webs/public/run2024/PbPb/js/')

    # lumisections = o.get_by_range(category = "lumisections",
    #                               var = "start_time", var2 = "end_time",
    #                               lmin = "2023-09-26T00:00", lmax = end_time,
    #                               per_page = 100, onlystable = True)
    # mega = lumisections[0]["meta"]
    # mega["lasttime"] = end_time
    # # lumisections = o.filter_data_list(lumisections, "beams_stable", True)
    # r_lumisections = translate(lumisections, ["start_time",
    #                                           "end_time",
    #                                           # "run_number",
    #                                           # "lumisection_number",
    #                                           "delivered_lumi",
    #                                           "recorded_lumi",
    #                                           "prescale_name",
    #                                           ], "lumisections")
    # f_lumisections = { "data": r_lumisections, "mega": mega }
    # with open('../cms-hin-coordination/webs/public/run/js/lumisections.js', 'w') as f:
    #     print('let lumisectioninfo = ', file = f)
    #     json.dump(f_lumisections, f, indent = 2)
