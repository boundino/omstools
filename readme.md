# Trigger rates and counts from OMS

* [Install](#install)
* [Usage](#usage)
    - [hltcount.py](#hltcountpy): HLT counts in given lumi section ranges of time range
    - [ratetable.py](#ratetablepy): HLT/L1 rates/counts comparison between run or lumi sections
    - [hltrunsummary.py](#hltrunsummarypy): HLT summary of a give run
    - [l1runsummary.py](#l1runsummarypy): L1 summary of a give run
    - [listruns.py](#listrunspy): Run list of a given time range

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
* Print HLT counts in given lumi ranges 
```
usage: hltcount.py [-h] (--lumiranges LUMIRANGES | --timerange TIMERANGE) --pathnames PATHNAMES [--outcsv OUTCSV]
options:
  -h, --help            show this help message and exit
  --lumiranges LUMIRANGES
                        (option 1) <min_run>(:<LS>)-<max_run>(:<LS>) e.g. 374763-374778,374797-374834; (option 2) cert json file
  --timerange TIMERANGE
                        (option 3) <start_time>,<end_time>
  --pathnames PATHNAMES
                        List of HLT paths, (option 1) HLT_1,HLT_2,HLT_3; (option 2) .txt file with each line as an HLT path
  --outcsv OUTCSV       Optional csv output file
```
* Example 1 (Use lumiranges)
    - Command
    ```
    python3 hltcount.py --lumiranges 374763-374778,374797-374834 --pathnames HLT_HIMinimumBiasHF1ANDZDC1nOR_v1,HLT_HIMinimumBiasHF1AND_v3
    ```
    - Screen
    ```
    Write to output file: outcsv/hltcount.csv
    Extracting lumisections with stable beams...
    Summing up lumi sections: {'374763': [[68, 106]], '374764': [[1, 31]], '374765': [[1, 28]], '374766': [[1, 34]], '374767': [[1, 32]], '374768': [[1, 31]], '374778': [[36, 287]], '374803': [[5, 592]], '374804': [[1, 14]], '374810': [[49, 1748]], '374828': [[24, 66]], '374833': [[67, 304]], '374834': [[1, 12]]}
    ------------------------------------------------------
    | HLT Path                          |          Count |
    ------------------------------------------------------
    | HLT_HIMinimumBiasHF1ANDZDC1nOR_v1 |     1031991933 |
    | HLT_HIMinimumBiasHF1AND_v3        |         811481 |
    ------------------------------------------------------
    ```

* Example 2 (Use json)
    - Command
    ```
    python3 hltcount.py --lumiranges examples/Cert_Collisions2022HISpecial_362293_362323_Golden.json --pathnames HLT_HIMinimumBias_v2
    ```
    - Screen
    ```
    Write to output file: outcsv/hltcount.csv
    Summing up lumi sections: {'362294': [[1, 53]], '362296': [[1, 59]], '362297': [[1, 199]], '362315': [[46, 96]], '362316': [[1, 18]], '362317': [[1, 11]], '362318': [[1, 58]], '362319': [[1, 24], [30, 50], [60, 66]], '362320': [[1, 193]], '362321': [[1, 356]], '362322': [[1, 31]], '362323': [[1, 416], [447, 590]]}
    -----------------------------------------
    | HLT Path             |          Count |
    -----------------------------------------
    | HLT_HIMinimumBias_v2 |       34031546 |
    -----------------------------------------
    ```

* Example 3 (Use time range)
    - Command
    ```
    python3 hltcount.py --timerange 2023-09-19T19:00,2023-09-20T05:00 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1
    ```
    - Screen
    ```
    Write to output file: outcsv/hltcount.csv
    Extracting lumisections with stable beams...
    Summing up lumi sections: {'373710': [[7, 832]]}
    --------------------------------------------
    | HLT Path                |          Count |
    --------------------------------------------
    | HLT_ZeroBias_v8         |         381927 |
    | HLT_PPRefGEDPhoton40_v1 |          44933 |
    | HLT_AK4PFJet100_v1      |          83279 |
    --------------------------------------------
    ```

### `ratetable.py`
* HLT paths or L1 rates or counts for a given set of runs/lumi sections
```
usage: ratetable.py [-h] --runls RUNLS --pathnames PATHNAMES [--l1preps] [--count] [--outcsv OUTCSV]

options:
  -h, --help            show this help message and exit
  --runls RUNLS         List of run with optional lumi section, e.g. 373710,373710:740
  --pathnames PATHNAMES
                        List of HLT paths or L1 seeds, (option 1) HLT_1,L1_1,L1_2 (option 2) .txt file with each line as an HLT/L1
  --l1preps             Optional store L1 pre PS rate instead of post DT rate
  --count               Optional store count instead of rate
  --outcsv OUTCSV       Optional csv output file
```
* Example
    - Command
    ```
    python3 ratetable.py --runls 373664,373710,373710:740 --pathnames examples/l1hlt.txt
    ```
    - Screen
    ```
    Variable option: rate
    L1 rate option: Post-DT after PS
    
    Write to output file: outcsv/ratetable.csv
                                                                                    [Hz]
    ------------------------------------------------------------------------------------
    | Path / L1 seed                         |      373664 |      373710 |  373710:740 |
    ------------------------------------------------------------------------------------
    | HLT_AK4CaloJet100_v1                   |       0.046 |       4.758 |       4.676 |
    | HLT_AK4PFJet100_v1                     |        0.02 |       4.148 |       3.904 |
    | HLT_PPRefDmesonTrackingGlobal_Dpt60_v1 |         0.0 |       0.128 |       0.129 |
    | HLT_PPRefEle50Gsf_v1                   |         0.0 |       0.124 |       0.086 |
    | HLT_PPRefGEDPhoton60_v1                |       0.008 |       0.526 |       0.686 |
    | HLT_PPRefZeroBias_v1                   |       7.907 |   18515.109 |    19887.81 |
    | L1_DoubleMuOpen                        |         0.0 |      90.062 |      90.215 |
    | L1_ZeroBias                            |       7.989 |   19731.539 |   19887.299 |
    | L1_SingleJet60                         |       0.856 |      74.919 |      71.726 |
    ------------------------------------------------------------------------------------
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
    python3 hltrunsummary.py --run 374810
    ```
    - Screen
    ```
    Run summary: [374810] (PB82 - PB82)
        Stable: Yes
        Time: 2023-10-05 23:17:16 - 2023-10-06 10:37:52
        Fill: 9232
        L1 menu: L1Menu_CollisionsHeavyIons2023_v1_1_3
        HLT menu: /cdaq/physics/Run2023HI/v1.1.3/HLT/V4
        HLT physics throughput: 11.98 GB/s
        L1 rate: 43008.45 Hz
        Lumi (recorded / delivered): 62.48 / 66.32 mub-1
    
    Write to output file: outcsv/hltrunsummary.csv
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | HLT Path                                                                         |      Rate (Hz) |        L1 Pass |   PS Pass |  Accepted | L1 seed                                            |
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ...
    | HLT_HIZeroBias_HighRate_v3                                                       |      970.25239 |       39624950 |  39624950 |  39624950 | L1_ZeroBias_copy                                   |
    | HLT_HIZeroBias_v10                                                               |      126.55733 |      214048776 |   5168581 |   5168581 | L1_ZeroBias                                        |
    | HLT_HcalCalibration_v6                                                           |       97.28214 |        3972987 |   3972987 |   3972987 | null                                               |
    | HLTriggerFinalPath                                                               |            0.0 |     1756425174 |1756425174 |         0 | null                                               |
    | HLTriggerFirstPath                                                               |            0.0 |     1756425174 |1756425174 |         0 | null                                               |
    | Status_OnCPU                                                                     |            0.0 |     1756425174 |1756425174 |         0 | null                                               |
    | Status_OnGPU                                                                     |    43007.64347 |     1756425174 |1756425174 |1756425174 | null                                               |
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------~
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
    Run summary: [374810] (PB82 - PB82)
        Stable: Yes
        Time: 2023-10-05 23:17:16 - 2023-10-06 10:37:52
        Fill: 9232
        L1 menu: L1Menu_CollisionsHeavyIons2023_v1_1_3
        HLT menu: /cdaq/physics/Run2023HI/v1.1.3/HLT/V4
        HLT physics throughput: 11.98 GB/s
        L1 rate: 43008.45 Hz
        Lumi (recorded / delivered): 62.48 / 66.32 mub-1
    
    Write to output file: outcsv/l1runsummary.csv
    ---------------------------------------------------------------------------------------------------------------------------------------
    |      |                                                                      |  Pre-DT [Hz] | Pre-DT [Hz] |   Post-DT | Post-DT [Hz] |
    |  Bit | Name                                                                 |    before PS |    after PS |      [Hz] |     from HLT |
    ---------------------------------------------------------------------------------------------------------------------------------------
    |   18 | L1_NotBptxOR                                                         |  26195441.75 |       10.01 |      9.46 |         9.45 |
    |   19 | L1_ZeroBias                                                          |  11335171.84 |     5420.36 |   5244.03 |      5241.04 |
    ...
    |  483 | L1_SingleJet20_NotMinimumBiasHF2_AND_BptxAND                         |       143.53 |      142.07 |     86.95 |         86.9 |
    |  484 | L1_SingleJet24_NotMinimumBiasHF2_AND_BptxAND                         |        63.22 |       63.22 |      34.9 |        34.88 |
    |  485 | L1_SingleJet28_NotMinimumBiasHF2_AND_BptxAND                         |        33.01 |       33.01 |     18.94 |        18.93 |
    ---------------------------------------------------------------------------------------------------------------------------------------
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
    python3 listruns.py --timemin 2023-10-01T04:00:00 --timemax 2023-10-01T18:00:00 --unit mub
    ```
    - Screen
    ```
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    |        |        |      |                     |                     |    Record |   Deliver |   L1 rate |     HLT |                                            |
    |    Run | Stable | Fill |          Start time |            End time |   (mub-1) |   (mub-1) |      (Hz) |  (GB/s) | HLT menu                                   |
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 374595 |   Yes  | 9213 | 2023-10-01 08:21:03 | 2023-10-01 09:23:02 |      5.79 |      6.24 |   10186.6 |    3.96 | /cdaq/physics/Run2023HI/v1.0.3/HLT/V3      |
    | 374596 |   Yes  | 9213 | 2023-10-01 09:25:45 | 2023-10-01 11:12:20 |      7.62 |      8.74 |   35759.3 |    10.4 | /cdaq/physics/Run2023HI/v1.0.3/HLT/V4      |
    | 374599 |   Yes  | 9213 | 2023-10-01 11:22:29 | 2023-10-01 11:45:04 |      1.01 |      1.07 |   37147.5 |    7.36 | /cdaq/physics/Run2023HI/v1.0.3/HLT/V4      |
    | 374612 |    No  | 9214 | 2023-10-01 15:04:04 | 2023-10-01 15:04:34 |       0.0 |      0.01 |     563.4 |     0.0 | /cdaq/physics/Run2023HI/v1.0.3/HLT/V4      |
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    ```
