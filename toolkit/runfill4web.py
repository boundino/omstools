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
            if not hltkey or ("PRef" not in hltkey
                              and "HI" not in hltkey
                              and "ppRef" not in hltkey
                              and "HeavyIon" not in hltkey
                              and "Protonion" not in hltkey):
                continue
            # trigger_mode = d["attributes"]["trigger_mode"]
            # if not trigger_mode or ("ppref_" not in trigger_mode and "_hi" not in trigger_mode):
            #     continue
            if not d["attributes"]["recorded_lumi"] or d["attributes"]["recorded_lumi"] <= 0:
                continue
            if not d["attributes"]["delivered_lumi"] or d["attributes"]["delivered_lumi"] <= 0:
                continue
            if not d["attributes"]["l1_rate"] or d["attributes"]["l1_rate"] <= 0:
                continue
            if not d["attributes"]["hlt_physics_throughput"] or d["attributes"]["hlt_physics_throughput"] <= 0:
                continue

        r = {}
        for k in keys:
            r[k] = d["attributes"][k]

        r["delivered_lumi_units"] = ""
        r["recorded_lumi_units"] = ""
        if "delivered_lumi" in d["meta"]["row"]:
            r["delivered_lumi_units"] = d["meta"]["row"]["delivered_lumi"]["units"]
        if "recorded_lumi" in d["meta"]["row"]:
            r["recorded_lumi_units"] = d["meta"]["row"]["recorded_lumi"]["units"]
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
        
    # runs = o.get_runs_by_time(start_time, end_time)

    runs_HIRun2024A = o.get_by_range(var = "era", lmin = "HIRun2024A", lmax = "HIRun2024B", category = "runs", per_page = 100)
    filljs(runs_HIRun2024A, '../cms-hin-coordination/webs/public/datasets/HIRun2024AB/js/')

    # runs_Run2024J = o.get_by_range(var = "era", lmin = "Run2024J", lmax = "Run2024J", category = "runs", per_page = 100)
    # filljs(runs_Run2024J, '../cms-hin-coordination/webs/public/datasets/Run2024J/js/')

    # runs_HIRun2023A = o.get_by_range(var = "era", lmin = "HIRun2023A", lmax = "HIRun2023A", category = "runs", per_page = 100)
    # filljs(runs_HIRun2023A, '../cms-hin-coordination/webs/public/datasets/HIRun2023A/js/')

    # runs_Run2023F = o.get_by_range(var = "era", lmin = "Run2023F", lmax = "Run2023F", category = "runs", per_page = 100)
    # filljs(runs_Run2023F, '../cms-hin-coordination/webs/public/datasets/Run2023F/js/')

    # runs_HIRun2022A = o.get_by_range(var = "era", lmin = "HIRun2022A", lmax = "HIRun2022A", category = "runs", per_page = 100)
    # filljs(runs_HIRun2022A, '../cms-hin-coordination/webs/public/datasets/HIRun2022A/js/')

    # runs_HIRun2018A = o.get_by_range(var = "era", lmin = "HIRun2018A", lmax = "HIRun2018A", category = "runs", per_page = 100)
    # filljs(runs_HIRun2018A, '../cms-hin-coordination/webs/public/datasets/HIRun2018A/js/')

    # runs_Run2017G = o.get_by_range(var = "era", lmin = "2017G", lmax = "2017G", category = "runs", per_page = 100)
    # filljs(runs_Run2017G, '../cms-hin-coordination/webs/public/datasets/Run2017G/js/')

    # runs_XeXeRun2017 = o.get_by_range(var = "era", lmin = "XeXeRun2017", lmax = "XeXeRun2017", category = "runs", per_page = 100)
    # filljs(runs_XeXeRun2017, '../cms-hin-coordination/webs/public/datasets/XeXeRun2017/js/')

    # runs_PARun2016C = o.get_by_range(var = "era", lmin = "PARun2016C", lmax = "PARun2016C", category = "runs", per_page = 100)
    # filljs(runs_PARun2016C, '../cms-hin-coordination/webs/public/datasets/PARun2016C/js/')

    # runs_PARun2016B = o.get_by_range(var = "era", lmin = "PARun2016B", lmax = "PARun2016B", category = "runs", per_page = 100)
    # filljs(runs_PARun2016B, '../cms-hin-coordination/webs/public/datasets/PARun2016B/js/')





