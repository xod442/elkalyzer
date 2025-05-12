import urllib3
from utility.workflow3 import find_version
import time


# There are two approaches to workflows, both using the session.
version = "10.09"
switch_user = 'admin'
switch_password = 'admin'

afc_list = ['10.250.201.11','10.250.202.11','10.250.203.11','10.250.204.11','10.250.205.11',\
'10.250.206.11','10.250.207.11','10.250.208.11','10.250.209.11','10.250.210.11']

counter = 0
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print('=======================================================================')
print("                       AFC / Switch Check                              ")


for afc in afc_list:
    print(afc)
    #switch_version = find_version(switch, version, switch_user, switch_password)
    #print('-------------------------------------------------------------------')
    #print("{} Switch is up and alive, running version {}.".format(switch, switch_version))
    #Zcounter = counter + 1
    #time.sleep(1)
#print("Total number of switches processed {}.".format(counter))
print('=======================================================================')
