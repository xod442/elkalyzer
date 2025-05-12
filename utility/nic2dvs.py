from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
from pyVim import connect
import time
import ssl
import logging
import atexit
from utility.write_line import write_line

def connect_to_vcenter(host, user, password, port=443):
    """
    Connect to vCenter server
    """
    try:
        sslContext = ssl._create_unverified_context()
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=password,
                                                port=port,
                                                sslContext=sslContext)
        atexit.register(connect.Disconnect, service_instance)
        return service_instance.RetrieveContent()
    except Exception as e:
        print("Unable to connect to vCenter server:", str(e))
        return None

    content = service_instance.RetrieveContent()

    return(content)

def get_dvs_by_name(content, dvs_name):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    for dvs in container.view:
        if dvs.name == dvs_name:
            return dvs
    return None

def check_dvs_uplinks(dvs):
    print(f"Checking uplinks for DVS: {dvs.name}")
    for host_member in dvs.config.host:
        host = host_member.config.host
        pnics = host_member.config.backing.pnicSpec
        line = f"\nHost: {host.name}"
        print(line)
        write_line(line)
        for spec in pnics:
            pnic_device = spec.pnicDevice
            try:
                # This part checks the physical NIC state on the host
                for pnic in host.config.network.pnic:
                    if pnic.device == pnic_device:
                        link_state = "Connected" if pnic.linkSpeed else "Disconnected"
                        line = f" - Uplink: {pnic.device} | MAC: {pnic.mac} | Status: {link_state}"
                        print(line)
                        write_line(line)
                        break
                else:
                    line = f" - Uplink: {pnic_device} not found in host physical NICs"
                    print(line)
                    write_line(line)
            except Exception as e:
                line = f" - Error checking {pnic_device}: {str(e)}"
                print(line)
                write_line(line)

def list_dvs_switches(content):
    dvs_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    dvs_list = dvs_view.view
    dvs_view.Destroy()
    return dvs_list
#
def get_vm_snapshot(vm):
    """
    Get the snapshot of a virtual machine.
    """
    if vm.snapshot is not None:
        return vm.snapshot.currentSnapshot
    return None

def wait_for_task(task, hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """
    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(5)
    return task.info.result

def get_dvswitches_and_portgroups(content):
    """
    Retrieve all distributed virtual switches and their associated port groups in the vCenter Server.
    """
    dvswitches = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    for switch in container.view:
        dvswitches[switch.name] = {'uuid': switch.uuid, 'portgroups': []}
        for pg in switch.portgroup:
            dvswitches[switch.name]['portgroups'].append(pg.name)
    container.Destroy()
    return dvswitches


def get_dvswitches_and_uplinks(content):
    """
    Retrieve all distributed virtual switches and their associated uplinks in the vCenter Server.
    """
    dvswitches = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    for switch in container.view:
        dvswitches[switch.name] = {'uuid': switch.uuid, 'uplinks': []}
        for uplink in switch.config.uplinkPortgroup:
            dvswitches[switch.name]['uplinks'].append(uplink.name)
    container.Destroy()
    return dvswitches

def get_dvswitches(content):
    """
    Retrieve all distributed virtual switches in the vCenter Server.
    """
    dvswitches = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    for switch in container.view:
        dvswitches[switch.name] = switch.uuid
    container.Destroy()
    return dvswitches

def list_networks(content):
    network_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Network], True)
    networks = network_view.view
    network_view.Destroy()
    return networks


# Function to find a virtual machine by its name
def find_vm_by_name(content, vm_name):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in container.view:
        if vm.name == vm_name:
            return vm
    return None

# Function to find a distributed virtual switch by its name
def find_dvs_by_name(content, dvs_name):
    dvs_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualSwitch], True)
    for switch in dvs_view.view:
        if switch.name == dvs_name:
            return switch
    return None

def get_dvportgroup_names(service_instance):
    content = service_instance.RetrieveContent()
    dvportgroups = content.viewManager.CreateContainerView(content.rootFolder, [vim.DistributedVirtualPortgroup], True)

    dvportgroup_names = []
    for dvportgroup in dvportgroups.view:
        dvportgroup_names.append(dvportgroup.name)

    return dvportgroup_names


def find_dvs_portgroup_by_name(content, dvs_name, portgroup_name):
    dvs = find_dvs_by_name(content, dvs_name)
    if dvs:
        #print(dvs_name)
        portgroup = find_portgroup_by_name(content, dvs, portgroup_name)
        return portgroup
    else:
        return None

def find_portgroup_by_name(content, dvs, portgroup_name):
    portgroup_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.dvs.DistributedVirtualPortgroup], True)
    portgroups = [pg for pg in portgroup_view.view if pg.config.distributedVirtualSwitch == dvs and pg.name == portgroup_name]
    portgroup_view.Destroy()
    if portgroups:
        return portgroups[0]
    else:
        return None

def connect_vnic_to_portgroup(dvs_name,dvs_pg,vm_name,vmnic_mac,portKey,vsp_ip,vsp_user,vsp_pass):
    """
    Connect vmnic to DVswitch.

    :variables:
        dvs_name            -type:string    'LG01-dvs-1'
        dvs_pg              -type:string    'LG01-DP-01'
        vm_name             -type:string    'LG01-WL01-V10-101'
        vmnic_mac           -type:string    '00:50:56:b6:5c:a6'
        portKey             -type:string    '1'
        vsp_ip              -type:string    '10.250.0.50'
        vsp_user            -type:string    'adminsitrator@vsphere.local'
        vsp_pass            -type:string    'my_pass'

    :return: None.
    """
    sslContext = ssl._create_unverified_context()
    port="443"

    # Create a connector to vsphere
    service_instance = SmartConnect(
                        host=vsp_ip,
                        user=vsp_user,
                        pwd=vsp_pass,
                        port=port,
                        sslContext=sslContext
    )
    if service_instance:

        content = service_instance.RetrieveContent()
        switch = find_dvs_by_name(content, dvs_name)
        # Get switch UUID
        switch_uuid = switch.uuid

        portgroup = find_dvs_portgroup_by_name(content, dvs_name, dvs_pg)
        if portgroup:
            vm = find_vm_by_name(content, vm_name)
            if vm:
                trash, portgroup_key = str(portgroup).split(':')
                portgroup_key = portgroup_key[:-1]

                devices = vm.config.hardware.device
                for device in devices:
                    if isinstance(device, vim.vm.device.VirtualVmxnet3):
                        if str(device.macAddress) == vmnic_mac:
                            nic_spec = vim.vm.device.VirtualDeviceSpec()
                            nic_spec.device = device
                            nic_spec.device.connectable.connected = True
                            nic_spec.device.deviceInfo.summary = dvs_pg
                            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                            nic_spec.device.backing.port.switchUuid = switch_uuid
                            nic_spec.device.backing.port.portgroupKey = portgroup_key
                            nic_spec.device.backing.port.portKey = portKey

                            config_spec = vim.vm.ConfigSpec(deviceChange=[nic_spec])
                            # Connect the port
                            task_number = vm.ReconfigVM_Task(config_spec)
                            response = wait_for_task(task_number)
                            print("Successfully connected vNIC with MAC {} to DVS port group.".format(vmnic_mac))
                            return


        #print("No vNIC found with MAC {} on the VM.".format(vmnic_mac))
    Disconnect(service_instance)
    return None
