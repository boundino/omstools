# Trigger rates and counts from OMS

## Install
```
git clone git@github.com:boundino/omstools.git
cd omstools/
pip3 install -r requirements.txt
```
- Add secret info in `.env`

## Usage
- Quick test
```
. examples/test.sh
```

### `hltcount.py`
- Print HLT counts in given lumi ranges of runs
```
options:
  -h, --help            show this help message and exit
  --lumiranges LUMIRANGES
                        e.g. 373664:25:30,373710 => <run>(:<minLS>:<maxLS>)
  --pathnames PATHNAMES
                        e.g. HLT_ZeroBias_v8,HLT_PPRefL1SingleMu7_v1
  --outcsv OUTCSV       Optional csv output file
```
- Example
```
python3 hltcount.py --lumiranges 373710:100:150 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1
```
- Screen
```
Write to output file: outcsv/hltcount.csv
Summing up lumi sections: {'373710': {'min': 100, 'max': 150}}
------------------------------------------------------------
|                                HLT Path |          Count |
------------------------------------------------------------
|                         HLT_ZeroBias_v8 |          23688 |
------------------------------------------------------------
|                 HLT_PPRefGEDPhoton40_v1 |           3075 |
------------------------------------------------------------
|                      HLT_AK4PFJet100_v1 |           5764 |
------------------------------------------------------------
```

### `hltrunsummary.py`
- Print HLT summary of a given run
```
options:
  -h, --help            show this help message and exit
  --run RUN             one run number
  --pathnames PATHNAMES
                        Optional HLT paths
  --outcsv OUTCSV       Optional csv output file
```
- Example
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
-----------------------------------------------------------------------------------------------------------------------------------------------
|                 HLT_PPRefGEDPhoton40_v1 |                           L1_SingleEG21 |        2.25688 |         996458 |    996458 |     53240 |
-----------------------------------------------------------------------------------------------------------------------------------------------
|                      HLT_AK4PFJet100_v1 |                          L1_SingleJet60 |        4.14754 |        1765972 |   1765972 |     97841 |
-----------------------------------------------------------------------------------------------------------------------------------------------
```
