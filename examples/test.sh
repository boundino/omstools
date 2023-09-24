set -x

python3 hltcount.py --lumiranges 373710:100:150 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1

certjson=/eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Collisions2022HISpecial/Cert_Collisions2022HISpecial_362293_362323_Golden.json
[[ -f $certjson ]] && python3 hltcount.py --lumiranges $certjson --pathnames HLT_HIMinimumBias_v2

python3 hltrunsummary.py --run 373710 --pathnames HLT_ZeroBias_v8,HLT_PPRefGEDPhoton40_v1,HLT_AK4PFJet100_v1

python3 hlttime.py --timemin 2023-09-19T18:00:00 --timemax 2023-09-20

set +x
