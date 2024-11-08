# Trigger rates and counts from OMS (supplemental tools)

* [Install](#install)
* [Usage](#usage)
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
