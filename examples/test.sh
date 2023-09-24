set -x

python3 hltcount.py --lumiranges 373710:100:150 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1

python3 hltrunsummary.py --run 373710 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1

python3 hlttime.py --timemin 2023-09-19T18:00:00 --timemax 2023-09-20

set +x
