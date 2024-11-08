python3 runfill4web.py # --timemin 2024-10-24T00:00:00
cd ../cms-hin-coordination/webs/public/
git diff run2024/PbPb/
git add run2024/PbPb/js/*.js
git commit -m "run"
git push origin master
cd -
