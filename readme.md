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
    - On lxplus
    ```
    git clone ssh://git@gitlab.cern.ch:7999/cmsoms/oms-api-client.git
    cd oms-api-client
    python3 setup.py install --user

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
* Print HLT counts in given lumi ranges of runs
```
options:
  -h, --help            show this help message and exit
  --lumiranges LUMIRANGES
                        <run>(:<minLS>:<maxLS>) e.g. 373664:25:30,373710 || (option 2) cert json file
  --pathnames PATHNAMES
                        e.g. HLT_ZeroBias_v8,HLT_PPRefL1SingleMu7_v1
  --outcsv OUTCSV       Optional csv output file
```
* Example 1
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

* Example 2
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

### `hltrunsummary.py`
* Print HLT summary of a given run
```
options:
  -h, --help            show this help message and exit
  --run RUN             one run number
  --pathnames PATHNAMES
                        Optional HLT paths
  --outcsv OUTCSV       Optional csv output file
```
* Example
    - Command
    ```
    python3 hltrunsummary.py --run 373710 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1
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
    -----------------------------------------------------------------------------------------------------------------------------------------------
    |                                HLT Path |                                 L1 seed |      Rate (Hz) |        L1 Pass |   PS Pass |  Accepted |
    -----------------------------------------------------------------------------------------------------------------------------------------------
    |                         HLT_ZeroBias_v8 |                             L1_ZeroBias |       19.70777 |      465028762 |    464909 |    464909 |
    |                 HLT_PPRefGEDPhoton40_v1 |                           L1_SingleEG21 |        2.25688 |         996458 |    996458 |     53240 |
    |                      HLT_AK4PFJet100_v1 |                          L1_SingleJet60 |        4.14754 |        1765972 |   1765972 |     97841 |
    -----------------------------------------------------------------------------------------------------------------------------------------------
    ```
