import util.oms as o
import util.utility as u
import json

def get_by_filter(key, filters = [], customs = []):
    q = o.omsapi.query(key)
    q.paginate(per_page = 3000)
    # q.set_verbose(False)
    q.set_validation(False)
    for c in customs:
        q.custom(c[0], c[1])
    for f in filters:
        q.filter(f[0], f[1], f[2])
    return q.data().json()

def save_json(d1, key):
    print(key)
    with open('toolkit/examples/'+key+'.json', 'w') as f:
        # print('let cadiinfo =', file = outputfile)
        json.dump(d1, f, indent = 2)
        

if __name__ == "__main__":
    # save_json(get_by_filter("l1algorithmtriggers",
    #                         [["run_number", "373710", "EQ"]],
    #                         [["group[granularity]", "run"]]), # lumisection
    #           "l1algorithmtriggers_run")

    # save_json(get_by_filter("l1algorithmtriggers",
    #                         # [["run_number", "373710", "EQ"], ["lumisection_number", 500, "EQ"]],
    #                         [["run_number", "373710", "EQ"], ["name", "L1_ZeroBias", "EQ"]],
    #                         [["group[granularity]", "lumisection"]]),
    #           "l1algorithmtriggers_lumisection")

    # save_json(get_by_filter("lumisections",
    #                         [["run_number", "374288", "EQ"]]),
    #           "lumisections")

    # save_json(get_by_filter("hltpathrates",
    #                         [["run_number", "374288", "EQ"], ["first_lumisection_number", 10, "GE"], ["last_lumisection_number", 12, "LE"], ["path_name", "HLT_HIUPC_ZeroBias_SinglePixelTrack_MaxPixelTrack_v6", "EQ"]]),
    #           "hltpathrates")

    # save_json(get_by_filter("l1configurationkeys",
    #                         [["run_number", "374925", "EQ"]]),
    #           "l1configurationkeys_374925")

    # save_json(get_by_filter("runs",
    #                         [["run_number", "374810", "EQ"]]),
    #           "runs")
    save_json(get_by_filter("filldetailx",
                            [["fill_number", "9232", "EQ"]]),
              "filldetailx")
