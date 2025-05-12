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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_version(key):

    device = Device(key)
    device.session = key
    version = device.get_firmware_version()

    return version
