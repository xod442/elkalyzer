import urllib3
from utility.connect import connect
from utility.get_version import get_version
from utility.get_lldp import get_lldp
import time
import subprocess
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import os
import sys
import logging
import json
import pyafc.session as session
import pyafc.devices as devices
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_version(switch,version,switch_user,switch_password):
    # Connect to cx switch and find software version
    switch = str(switch)
    key = connect(switch, version, switch_user, switch_password)
    version = get_version(key)
    key.close()

    return version

def get_switches(base_url, afc_user, afc_password):
    login_session, auth_header = session.login(base_url, afc_user, afc_password)
    session_dict = dict(s=login_session, url=base_url)
    switches = devices.get_all_switches(auth_header, **session_dict)

    return switches

def lldp(switch,version,switch_user,switch_password):
    # Connect to cx switch and find software version
    switch = str(switch)
    key = connect(switch, version, switch_user, switch_password)
    lldp_info = get_lldp(key)
    key.close()

    return lldp_info
