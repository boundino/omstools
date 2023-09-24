from omsapi import OMSAPI
import os
import env

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

def print_run(data):
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
    print("    HLT physics throughput: \033[4m" + str(round(attr["hlt_physics_throughput"], 2)) + "\033[0m GB/s")
    print("    L1 rate: \033[4m" + str(attr["l1_rate"]) + "\033[0m Hz")
    print("    Lumi (recorded / delivered): \033[4m" + str(round(attr["recorded_lumi"]*1.e3, 2)) + "\033[0m / \033[4m" + str(round(attr["delivered_lumi"]*1.e3, 2)) + "\033[0m nb-1")

def print_run_line(data):
    attr = data["attributes"]

    if attr["stable_beam"]:
        print('|{:>7} | \033[32;1m{:>6}\033[0m '.format(data["id"], "Yes"), end = "")
    else:
        print('|{:>7} | \033[31;1m{:>6}\033[0m '.format(data["id"], "No"), end = "")
         
    print('|{:>5} |{:>20} |{:>20} |{:>16} |{:>17} |{:>10} |{:>11} |{:>45} |'.format(attr["fill_number"],
                                                                                attr["start_time"].replace("T", " ").replace("Z", ""), attr["end_time"].replace("T", " ").replace("Z", ""),
                                                                                round(attr["recorded_lumi"]*1.e3, 2), round(attr["delivered_lumi"]*1.e3, 2),
                                                                                attr["l1_rate"], round(attr["hlt_physics_throughput"], 2),
                                                                                attr["hlt_key"]))
    
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

def print_lumi_info(d):
    attr = d["attributes"]
    print('    {:>5}'.format(attr["lumisection_number"]), end = "")
    if attr["beams_stable"]:
        print('\033[32;1m{:>9}\033[0m'.format("Stable"), end = "")
    else:
        print('\033[31;1m{:>9}\033[0m'.format("No"), end = "")

    print('{:>23} {:>23} {:>10} {:>10}'.format(attr["start_time"].replace("T", " ").replace("Z", ""),
                                  attr["end_time"].replace("T", " ").replace("Z", ""),
                                  round(attr["delivered_lumi"]*1.e3, 3),
                                  round(attr["recorded_lumi"]*1.e3, 3)
                                  ))

