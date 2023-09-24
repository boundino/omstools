from omsapi import OMSAPI
import os
import sys
import env
import util.utility as u

my_app_id = env.CLIENT_ID
my_app_secret = env.CLIENT_SECRET

# from dotenv import load_dotenv
# load_dotenv()
# my_app_id = os.getenv('CLIENT_ID')
# my_app_secret = os.getenv('CLIENT_SECRET')

omsapi = OMSAPI("https://cmsoms.cern.ch/agg/api", "v1", cert_verify = False)
omsapi.auth_oidc(my_app_id, my_app_secret, audience = "cmsoms-prod")

def get_item_data(jsdata, key, value):
    for ii in jsdata:
        if key in ii["attributes"]:
            if ii["attributes"][key] == value:
                return ii
    return None

def get_run_info(run, verbose, omsapi = omsapi):
    q = omsapi.query("runs")
    q.set_verbose(False)
    q.filter("run_number", run)
    data = q.data().json()["data"]
    if not data:
        print("\033[31merror: run number: \"\033[4m" + run + "\033[0m\033[31m\", skip it..\033[0m")
        return None

    if verbose:
        print()
        print_run(data[0])

    return data[0]

def print_run(data, tounit = "mub"):
    attr = data["attributes"]
    print("Run summary: [\033[1;4m" + data["id"] + "\033[0m] (\033[1;4m" + attr["fill_type_party1"] + " - " + attr["fill_type_party2"] + "\033[0m)")
    print("    Stable: ", end = "")
    if attr["stable_beam"]:
        print("\033[32;1mYes\033[0m")
    else:
        print("\033[31;1mNo\033[0m")
    print("    Time: " + attr["start_time"].replace("T", " ").replace("Z", "") + " - " + attr["end_time"].replace("T", " ").replace("Z", ""))
    for att in [{ "key" : "fill_number", "desc" : "Fill"}, {"key" : "l1_menu", "desc" : "L1 menu"}, {"key" : "hlt_key", "desc" : "HLT menu"}]:
        if attr[att["key"]]:
            print("    "+att["desc"]+": \033[4m" + str(attr[att["key"]]) + "\033[0m")
        else:
            print("    "+att["desc"]+": \033[4mNone\033[0m")

    delivered_lumi_unit = u.translate_lumi_unit(data["meta"]["row"]["delivered_lumi"]["units"], tounit)
    recorded_lumi_unit = u.translate_lumi_unit(data["meta"]["row"]["recorded_lumi"]["units"], tounit)
    
    print("    HLT physics throughput: \033[4m" + str(round(attr["hlt_physics_throughput"], 2)) + "\033[0m GB/s")
    print("    L1 rate: \033[4m" + str(attr["l1_rate"]) + "\033[0m Hz")
    print("    Lumi (recorded / delivered): \033[4m" + str(round(attr["recorded_lumi"]*recorded_lumi_unit, 2)) + "\033[0m / \033[4m" + str(round(attr["delivered_lumi"]*delivered_lumi_unit, 2)) + "\033[0m mub-1")

def print_run_line(data, tounit = "mub"):
    attr = data["attributes"]

    if attr["stable_beam"]:
        print('|{:>7} | \033[32;7m{:>5} \033[0m '.format(data["id"], "Yes"), end = "")
    else:
        print('|{:>7} | \033[31;7m{:>5} \033[0m '.format(data["id"], "No"), end = "")

    delivered_lumi_unit = u.translate_lumi_unit(data["meta"]["row"]["delivered_lumi"]["units"], tounit)
    recorded_lumi_unit = u.translate_lumi_unit(data["meta"]["row"]["recorded_lumi"]["units"], tounit)
    
    print('|{:>5} |{:>20} |{:>20} |{:>8} |{:>8} |{:>10} |{:>8} |{:>42} |'.format(attr["fill_number"],
                                                                                 attr["start_time"].replace("T", " ").replace("Z", ""), attr["end_time"].replace("T", " ").replace("Z", ""),
                                                                                 round(attr["recorded_lumi"]*recorded_lumi_unit, 2), round(attr["delivered_lumi"]*delivered_lumi_unit, 2),
                                                                                 round(attr["l1_rate"], 1), round(attr["hlt_physics_throughput"], 2),
                                                                                 attr["hlt_key"]))

def print_run_title(onlyline = False, unit = "mub"):
    if not onlyline:
        print('-' * 156)
        print('|{:>7} | {:>6} |{:>5} |{:>20} |{:>20} |{:>8} |{:>8} |{:>10} |{:>8} |{:>42} |'.format("", "", "",
                                                                                                    "", "",
                                                                                                    "Record", "Deliver",
                                                                                                    "L1 rate", "HLT", ""))
        print('|{:>7} | {:>6} |{:>5} |{:>20} |{:>20} |{:>8} |{:>8} |{:>10} |{:>8} |{:>42} |'.format("Run", "Stable", "Fill",
                                                                                                    "Start time", "End time",
                                                                                                    "("+unit+"-1)", "("+unit+"-1)",
                                                                                                    "(Hz)", "(GB/s)", "HLT menu")) 
    print('-' * 156)
    
def get_lumis_by_run(run, omsapi = omsapi):
    q = omsapi.query("lumisections")
    q.paginate(per_page = 3000)
    q.set_verbose(False)
    q.filter("run_number", run)
    data = q.data().json()["data"]
    if not data:
        print("\033[31merror: run number: \"\033[4m" + run + "\033[0m\033[31m\", skip it..\033[0m")
        return None
    return data

def get_json_by_lumi(data):
    lumijson = {}
    for ls in data:
        thisrun = str(ls["attributes"]["run_number"])
        thisls = ls["attributes"]["lumisection_number"]
        if thisrun not in lumijson:
            lumijson[thisrun] = []
        lumijson[thisrun].append(thisls)

    for run in lumijson:
        lumiranges = u.merge_json_array(lumijson[run])
        lumijson[run] = lumiranges

    return lumijson

def get_hltconfig_info(key, omsapi = omsapi):
    q = omsapi.query("hltconfigdata")
    q.paginate(per_page = 1000)
    q.set_verbose(False)
    q.filter("config_name", key)
    data = q.data().json()["data"]
    if not data:
        print("\033[31merror: config_name: \"\033[4m" + key + "\033[0m\033[31m\", skip it..\033[0m")
        return None
    return data

def print_lumi_info(d, tounit = "mub"):
    attr = d["attributes"]
    print('    {:>5}'.format(attr["lumisection_number"]), end = "")
    if attr["beams_stable"]:
        print('\033[32;1m{:>9}\033[0m'.format("Stable"), end = "")
    else:
        print('\033[31;1m{:>9}\033[0m'.format("No"), end = "")

    delivered_lumi_unit = u.translate_lumi_unit(d["meta"]["row"]["delivered_lumi"]["units"], tounit)
    recorded_lumi_unit = u.translate_lumi_unit(d["meta"]["row"]["recorded_lumi"]["units"], tounit)
        
    print('{:>18} {:>18} {:>10} {:>10}'.format(attr["start_time"].replace("T", " ").replace("Z", ""),
                                  attr["end_time"].replace("T", " ").replace("Z", ""),
                                  round(attr["delivered_lumi"]*delivered_lumi_unit, 3),
                                  round(attr["recorded_lumi"]*recorded_lumi_unit, 3)
                                  ))

def get_runs_by_time(start_time, end_time, category = "runs"):
    q = omsapi.query(category)
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
            print("\033[31merror: no interesting " + category + " during: \"\033[4m" + start_time + ", " + end_time + "\033[0m\033[31m\", give up..\033[0m")
            sys.exit()
        datas.extend(data)
        if qjson["links"]["next"] is None:
            break;
        ipage = ipage+1
    return datas

def get_hltlist_by_run(run):
    q = omsapi.query("hltpathinfo")
    q.set_verbose(False)
    q.paginate(per_page = 3000)
    q.filter("run_number", run)
    data = q.data().json()["data"]
    
    hltlist = []
    for d in data:
        hltlist.append(d["attributes"]["path_name"])

    return hltlist
