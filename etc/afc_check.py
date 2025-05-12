import urllib3
from utility.workflow3 import find_version
from utility.workflow3 import get_switches
import time
from utility.write_line import write_line
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# There are two approaches to workflows, both using the session.
version = "10.09"
afc_user = 'admin'
afc_password = 'admin'
serno = open('serial.txt','w')
cr = '\n'

afc_list = ['10.250.201.11','10.250.202.11','10.250.203.11','10.250.204.11','10.250.205.11',\
'10.250.206.11','10.250.207.11','10.250.208.11','10.250.209.11','10.250.210.11']
# afc_list = ['10.250.201.11']
counter = 0
c = ','
line = '======================================================================='
print(line)
write_line(line)
line = "                       AFC / Switch Check                              "
print(line)
write_line(line)

counter = 0
for afc_ip in afc_list:
    base_url = "https://{0}/api/v1/".format(afc_ip)
    line = "======------------AFC INFO -------------================================="
    print(line)
    write_line(line)

    line = "{} is the baseurl.".format(base_url)
    print(line)
    write_line(line)

    switches = get_switches(base_url, afc_user, afc_password)
    for s in switches:
        line = "{} Switch is discovered, and it's status is {}.".format(s['ip_address'], s['status'])
        print(line)
        write_line(line)
        inventory = str(s['name'])+c+str(s['description'])+c+str(s['mac_address'])+c+str(s['ip_address'])+c+str(s['sw_version'])+c+str(s['serial_number'])
        serno.write(inventory)
        serno.write(cr)
    #print('-------------------------------------------------------------------')
    #print("{} Switch is up and alive, running version {}.".format(switch, switch_version))
    counter = counter + 1
    #time.sleep(1)
#print("Total number of switches processed {}.".format(counter))
line = '=======================  END AFC CHECK  ==============================='
print(line)
write_line(line)
serno.close()
