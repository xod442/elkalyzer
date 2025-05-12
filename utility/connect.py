from pyaoscx.session import Session
from pyaoscx.device import Device
from pyaoscx.configuration import Configuration
import pyaoscx.firmware as firm
from pyaoscx.pyaoscx_factory import PyaoscxFactory

def connect(switch, version, switch_user, switch_password):
    s = Session(switch, version)
    s.open(switch_user, switch_password, use_proxy=False)

    return s
