from utility.afc_list import afc_list
from utility.psm_list import psm_list
from utility.switch_list import switch_list
from utility.workload_list import workload_list
from utility.connect import connect

from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import logging

from pyaoscx.session import Session
from pyaoscx.device import Device
from pyaoscx.configuration import Configuration
import pyaoscx.firmware as firm
from pyaoscx.pyaoscx_factory import PyaoscxFactory
import urllib3
import datetime
import utility.writer as w

import logging
import ssl
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Clear text file
f = open('lab_check.txt', 'w')
cr = '\n'
initx = '-'
f.write(initx)
f.write(cr)
f.close()

w.divider()
message = ' Lab health check is running......version 1.0....stand-by'
w.write_header(message)

'''
==========================================================================
CHeck switch available and version
==========================================================================
'''
switch_list = [
'10.205.201.101',
'10.205.201.102',
'10.205.201.103',
'10.205.202.101',
'10.205.202.102',
'10.205.202.103',
'10.205.203.101',
'10.205.203.102',
'10.205.203.103',
'10.205.204.101'
]

counter = 1
switch_user = 'admin'
switch_password = 'admin'
version = "10.04"
message = 'Listing available switches...'
w.write_line(message)

for s in switch_list:
    key = connect(s, version, "admin", "admin")
    fw = key.firm.get_firmware_version()
    print(fw)
    key.close()

    #fw = s.firm.get_get_firmware_version()

    #write_line(firmware_version)
    #w.write_line(firmware_version)
    counter = counter + 1

'''
==========================================================================
Check Aruba Fabric Composer
==========================================================================
'''
'''
==========================================================================
Check Pensando
==========================================================================
'''
'''
==========================================================================
Verify Workloads
==========================================================================
'''
'''
==========================================================================
Verify Distributed Virtual Switches
==========================================================================
'''
