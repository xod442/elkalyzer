import urllib3

from pyaoscx.session import Session
from pyaoscx.device import Device
from pyaoscx.lldp_neighbor import LLDPNeighbor
from pyaoscx.pyaoscx_factory import PyaoscxFactory
from utility.connect import connect
import pyaoscx.firmware as firm
from utility.afc_list import afc_list
from utility.psm_list import psm_list
from utility.switch_list import switch_list
from utility.workload_list import workload_list
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_lldp(key):

    lldp = LLDPNeighbor(key)
    lldp.session = key
    lldp_info = lldp.get_facts()

    return lldp_info
