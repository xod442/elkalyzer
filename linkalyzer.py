from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import atexit

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
        print(f"\nHost: {host.name}")
        for spec in pnics:
            pnic_device = spec.pnicDevice
            try:
                # This part checks the physical NIC state on the host
                for pnic in host.config.network.pnic:
                    if pnic.device == pnic_device:
                        link_state = "Connected" if pnic.linkSpeed else "Disconnected"
                        print(f" - Uplink: {pnic.device} | MAC: {pnic.mac} | Status: {link_state}")
                        break
                else:
                    print(f" - Uplink: {pnic_device} not found in host physical NICs")
            except Exception as e:
                print(f" - Error checking {pnic_device}: {str(e)}")

def main():
    # Replace with your vCenter info
    vc_host = "your_vcenter_host"
    vc_user = "your_username"
    vc_password = "your_password"
    dvs_name = "Your_DVS_Name"

    # Skip SSL verification
    context = ssl._create_unverified_context()
    si = SmartConnect(host=vc_host, user=vc_user, pwd=vc_password, sslContext=context)
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    dvs = get_dvs_by_name(content, dvs_name)
    if not dvs:
        print("Distributed Virtual Switch not found.")
        return

    check_dvs_uplinks(dvs)

if __name__ == "__main__":
    main()
