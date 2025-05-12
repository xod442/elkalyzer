import urllib3

from pyaoscx.session import Session
from pyaoscx.device import Device
from pyaoscx.pyaoscx_factory import PyaoscxFactory
from utility.connect import connect
import pyaoscx.firmware as firm
from utility.afc_list import afc_list
from utility.psm_list import psm_list
from utility.switch_list import switch_list
from utility.workload_list import workload_list
from utility.get_version import get_version
import subprocess
from utility.workflow3 import find_version


# There are two approaches to workflows, both using the session.
version = "10.09"
switch_user = 'admin'
switch_password = 'admin'

switch = '10.250.202.102'
counter = 0
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

version = find_version(switch, version, switch_user, switch_password)
print("{} Switch is up and alive, running version {}.".format(switch, version))
