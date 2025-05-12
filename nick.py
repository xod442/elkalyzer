from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import logging
import utility.nic2dvs as nic
from utility.vm_watcher import vm_watcher


dvs_name = 'LG01-dvs-1'
dvs_pg = 'LG01-ELK-99'
vm_name ='LG01-ELK'
vmnic_mac = '00:50:56:b6:1f:9f'
portKey = '5'
vsp_ip = '10.250.0.50'
vsp_user = 'administrator@vsphere.local'
vsp_pass = "Aruba123!@#"

portgroup_name = 'LG05-vlan20'

content = nic.connect_to_vcenter(vsp_ip,vsp_user,vsp_pass)

dvs_info = nic.list_dvs_switches(content)

print(dvs_info)
if dvs_info:

    for dvs in dvs_info:
        print(dvs.name)
        response = nic.check_dvs_uplinks(dvs)

# info = nic.get_dvswitches_and_portgroups(content)
