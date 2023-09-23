from omsapi import OMSAPI
import os
from dotenv import load_dotenv

load_dotenv()

my_app_id = os.getenv('CLIENT_ID')
my_app_secret = os.getenv('CLIENT_SECRET')

omsapi = OMSAPI("https://cmsoms.cern.ch/agg/api", "v1", cert_verify = False)
omsapi.auth_oidc(my_app_id, my_app_secret, audience = "cmsoms-prod")
