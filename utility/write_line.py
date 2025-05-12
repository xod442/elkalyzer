import urllib3
import datetime

import logging
import ssl
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def write_line(message):
    logging.basicConfig(filename="lab_check.log",
        				format='%(asctime)s %(message)s',
        				filemode='a')

    # Set up file handler and carrige return
    f = open('lab_check.txt', 'a')
    cr = '\n'

    logging.warning(message)
    f.write(message)
    f.write(cr)
    f.close()
