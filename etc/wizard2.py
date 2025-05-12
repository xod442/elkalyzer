#!/usr/bin/env python3
'''
Data Center POD automatio information
2024 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0.

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "0.1.1"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Alpha"
'''

from requests.packages.urllib3.exceptions import InsecureRequestWarning

import urllib3
import requests
import os
import sys
import logging
import json
import pyafc.session as session
import pyafc.devices as devices
import time

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)

# Get data centrer variables
afc_user = 'admin'
afc_password = 'admin'
afc_ip = '10.250.201.11'
base_url = "https://{0}/api/v1/".format(afc_ip)

# Build the data center

print('login')
login_session, auth_header = session.login(base_url, afc_user, afc_password)
session_dict = dict(s=login_session, url=base_url)
print(session_dict)
device = devices.get_all_switches(auth_header, **session_dict)
for dev in device:
    print(dev['ip_address'])
#session.logout(auth_header, **session_dict)
