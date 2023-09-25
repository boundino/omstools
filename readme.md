# Trigger rates and counts from OMS

## Install
```
git clone git@github.com:boundino/omstools.git
cd omstools/
```
* Add requirements
    - On private computer
    ```
    pip3 install -r requirements.txt # private pc
    ```
    - On lxplus8
    ```
    git clone ssh://git@gitlab.cern.ch:7999/cmsoms/oms-api-client.git
    cd oms-api-client
    python3 setup.py install --user
    python3.8 setup.py bdist_rpm --python /usr/bin/python3.8 --build-requires python38,python38-setuptools --release 0.el8
    ```

* Add secret info (ask me) in `env.py`
```
CLIENT_ID = 'example_id'
CLIENT_SECRET = 'example_secret'
```

## Usage
* Quick test
```
./examples/test.sh
```

### `hltcount.py`
* Print HLT counts in given lumi ranges of run:lumis
```
usage: hltcount.py [-h] (--lumiranges LUMIRANGES | --timerange TIMERANGE) --pathnames PATHNAMES [--outcsv OUTCSV]

options:
  -h, --help            show this help message and exit
  --lumiranges LUMIRANGES
                        (option 1) <run>(:<minLS>:<maxLS>) e.g. 373664:25:30,373710 || (option 2) cert json file
  --timerange TIMERANGE
                        (option 3) <start_time>,<end_time>
  --pathnames PATHNAMES
                        e.g. HLT_ZeroBias_v8,HLT_PPRefL1SingleMu7_v1
  --outcsv OUTCSV       Optional csv output file
```
* Example 1 (Use lumiranges)
    - Command
    ```
    python3 hltcount.py --lumiranges 373710:100:150 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1
    ```
    - Screen
    ```
    Write to output file: outcsv/hltcount.csv
    Summing up lumi sections: {'373710': [[100, 150]]}
    ------------------------------------------------------------
    |                                HLT Path |          Count |
    ------------------------------------------------------------
    |                         HLT_ZeroBias_v8 |          23688 |
    |                 HLT_PPRefGEDPhoton40_v1 |           3075 |
    |                      HLT_AK4PFJet100_v1 |           5764 |
    ------------------------------------------------------------
    ```

* Example 2 (Use json)
    - Command
    ```
    python3 hltcount.py --lumiranges Cert_Collisions2022HISpecial_362293_362323_Golden.json --pathnames HLT_HIMinimumBias_v2
    ```
    - Screen
    ```
    Write to output file: outcsv/hltcount.csv
    Summing up lumi sections: {'362294': [[1, 53]], '362296': [[1, 59]], '362297': [[1, 199]], '362315': [[46, 96]], '362316': [[1, 18]], '362317': [[1, 11]], '362318': [[1, 58]], '362319': [[1, 24], [30, 50], [60, 66]], '362320': [[1, 193]], '362321': [[1, 356]], '362322': [[1, 31]], '362323': [[1, 416], [447, 590]]}
    ------------------------------------------------------------
    |                                HLT Path |          Count |
    ------------------------------------------------------------
    |                    HLT_HIMinimumBias_v2 |       34031546 |
    ------------------------------------------------------------
    ```

* Example 3 (Use time range)
    - Command
    ```
    python3 hltcount.py --timerange 2023-09-19T19:00,2023-09-20T05:00 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1
    ```
    - Screen
    ```
    Write to output file: outcsv/hltcount.csv
    Summing up lumi sections: {'373664': [[62, 194]], '373681': [[1, 45], [47, 134]], '373697': [[1, 151]], '373703': [[1, 112]], '373705': [[1, 186]], '373710': [[1, 832]]}
    ------------------------------------------------------------
    |                                HLT Path |          Count |
    ------------------------------------------------------------
    |                         HLT_ZeroBias_v8 |         410750 |
    |                 HLT_PPRefGEDPhoton40_v1 |          45441 |
    |                      HLT_AK4PFJet100_v1 |          83710 |
    ------------------------------------------------------------
    ```

### `hltrunsummary.py`
* Print HLT summary of a given run
```
usage: hltrunsummary.py [-h] --run RUN [--outcsv OUTCSV]

options:
  -h, --help       show this help message and exit
  --run RUN        one run number
  --outcsv OUTCSV  Optional csv output file
```
* Example
    - Command
    ```
    python3 hltrunsummary.py --run 373710 
    ```
    - Screen
    ```
    Run summary: [373710] (PROTON - PROTON)
        Stable: Yes
        Time: 2023-09-19 23:37:31 - 2023-09-20 06:10:43
        Fill: 9168
        L1 menu: L1Menu_CollisionsPPRef2023_v1_1_0
        HLT menu: /cdaq/physics/Run2023/PRef/v1.0.2/HLT/V1
        HLT physics throughput: 2.49 GB/s
        L1 rate: 44106.65 Hz
        Lumi (recorded / delivered): 417.27 / 427.04 nb-1
    
    Write to output file: outcsv/hltrunsummary.csv
    --------------------------------------------------------------------------------------------------------------------------------------------------------------
    |                                     HLT Path |      Rate (Hz) |        L1 Pass |   PS Pass |  Accepted |                                           L1 seed |
    --------------------------------------------------------------------------------------------------------------------------------------------------------------
    |                         HLT_AK4CaloJet100_v1 |        4.75843 |        1765972 |   1765972 |    112252 |                                    L1_SingleJet60 |
    |                         HLT_AK4CaloJet120_v1 |        1.99011 |         268428 |    268428 |     46947 |                                    L1_SingleJet90 |
    |                          HLT_AK4CaloJet40_v1 |            0.0 |      465028762 |         0 |         0 |                                       L1_ZeroBias |
    ......
    |                      HLT_ZDCCommissioning_v1 |            0.0 |      465028762 |         0 |         0 |                                       L1_ZeroBias |
    |                     HLT_ZeroBias_Beamspot_v9 |       13.18594 |      465028762 |    464909 |    311058 |                                       L1_ZeroBias |
    |  HLT_ZeroBias_FirstCollisionAfterAbortGap_v7 |        4.93346 |         232890 |    116381 |    116381 |                          L1_FirstCollisionInOrbit |
    |                              HLT_ZeroBias_v8 |       19.70777 |      465028762 |    464909 |    464909 |                                       L1_ZeroBias |
    --------------------------------------------------------------------------------------------------------------------------------------------------------------
    ```

### `l1runsummary.py`
* Print L1 trigger summary of a given run
```
usage: l1runsummary.py [-h] --run RUN [--outcsv OUTCSV] [--compress]

options:
  -h, --help       show this help message and exit
  --run RUN        one run number
  --outcsv OUTCSV  Optional csv output file
  --compress       Optional filter turned-on bits
```
* Example
    - Command
    ```
    python3 l1runsummary.py --run 373710 --compress
    ```
    - Screen
    ```
    Write to output file: outcsv/l1runsummary.csv
    ------------------------------------------------------------------------------------------------------------------------------
    |      |                                                             |  Pre-DT [Hz] | Pre-DT [Hz] |   Post-DT | Post-DT [Hz] |
    |  Bit |                                                        Name |    before PS |    after PS |      [Hz] |     from HLT |
    ------------------------------------------------------------------------------------------------------------------------------
    |    1 |                                                 L1_ZeroBias |    447587.16 |    19901.61 |  19731.54 |     19712.18 |
    |   18 |                                                L1_NotBptxOR |  38554582.75 |       49.89 |     48.73 |        48.72 |
    |   26 |                                    L1_FirstCollisionInOrbit |     11189.68 |        9.96 |      9.88 |         9.87 |
    ......
    |  320 |                                       L1_SingleJet35_FWD2p5 |        75.67 |       75.67 |     74.64 |        74.57 |
    |  321 |                                       L1_SingleJet60_FWD2p5 |         4.72 |        4.72 |      4.65 |         4.64 |
    |  322 |                                       L1_SingleJet90_FWD2p5 |         0.63 |        0.63 |      0.62 |         0.62 |
    |  323 |                                      L1_SingleJet120_FWD2p5 |         0.12 |        0.12 |      0.12 |         0.12 |
    ------------------------------------------------------------------------------------------------------------------------------~
    ```

### `listruns.py`
* Print runs of interest in a given time range
```
usage: listruns.py [-h] --timemin TIMEMIN [--timemax TIMEMAX] [--stable] [--unit {mub,nb,pb}]

options:
  -h, --help          show this help message and exit
  --timemin TIMEMIN   Start date, e.g. 2023-09-19T18:00:00
  --timemax TIMEMAX   Optional End date, e.g. 2023-09-20
  --stable            Optional requiring stable beam runs
  --unit {mub,nb,pb}  Optional lumi unit
```
* Example
    - Command
    ```
    python3 listruns.py --timemin 2018-11-28T04:00:00 --timemax 2018-11-28T18:00:00 --unit mub
    ```
    - Screen
    ```
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    |        |        |      |                     |                     |  Record | Deliver |   L1 rate |     HLT |                                           |
    |    Run | Stable | Fill |          Start time |            End time | (mub-1) | (mub-1) |      (Hz) |  (GB/s) |                                  HLT menu |
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 327403 |   Yes  | 7480 | 2018-11-28 04:45:37 | 2018-11-28 07:05:04 |    9.21 |    9.57 |   30746.0 |    0.98 |     /cdaq/physics/Run2018HI/v2.0.0/HLT/V2 |
    | 327418 |    No  | 7481 | 2018-11-28 08:31:31 | 2018-11-28 08:58:17 |     0.0 |     0.0 |    1196.6 |    0.01 |     /cdaq/physics/Run2018HI/v2.0.0/HLT/V2 |
    | 327424 |   Yes  | 7481 | 2018-11-28 09:41:35 | 2018-11-28 10:14:26 |    4.24 |     8.2 |   10773.7 |    0.62 |     /cdaq/physics/Run2018HI/v2.0.0/HLT/V2 |
    | 327430 |   Yes  | 7481 | 2018-11-28 10:23:53 | 2018-11-28 17:26:17 |   60.74 |    62.6 |   22326.7 |    1.37 |     /cdaq/physics/Run2018HI/v2.0.0/HLT/V2 |
    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    ```
