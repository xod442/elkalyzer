import urllib3
import utility.nic2dvs as nic
import time
from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import logging
from utility.write_line import write_line

def vm_watcher(content, name):

    vm = nic.find_vm_by_name(content, name)
    devices = vm.config.hardware.device
    for device in devices:
        if isinstance(device, vim.vm.device.VirtualVmxnet3):
            if device.connectable.connected == True:
                state = 'nic is connected'
                line = "Workload: {} MAC address: {} connected state {}.".format(name, device.macAddress, device.connectable.connected)
                print(line)
                write_line(line)
            else:
                line = "Workload: {} MAC address: {} IS NOT CONNECTED!!!!.".format(name, device.macAddress)
                print(line)
                write_line(line)
            if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
                snapshot = nic.get_vm_snapshot(vm)
                if snapshot:
                    line = "Workload: {} is powered on and is running snapshot {}.".format(name, snapshot)
                    print(line)
                    write_line(line)
                else:
                    line = "Workload: {} MAC address: {} IS NOT CONNECTED!!!!.".format(name, device.macAddress)
                    print(line)
                    write_line(line)
