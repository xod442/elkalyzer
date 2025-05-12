import urllib3
import datetime

import logging
import ssl
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logging.basicConfig(filename="lab_check.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

def divider():
    counter = 1
    bar = '============================================================='
    message = '-----DCN ILT -- V L A B    C H E C K  1.0 -------------------'
    f = open('lab_check.txt', 'a')
    cr = '\n'
    f.write(bar)
    f.write(cr)
    logging.warning(bar)
    f.write(message)
    f.write(cr)
    logging.warning(message)

    while counter < 8:
        f.write(bar)
        f.write(cr)
        counter = counter + 1


def write_header(message):
    # Set up file handler and carrige return
    f = open('lab_check.txt', 'a')
    cr = '\n'
    bar = '============================================================='
    logging.warning(bar)
    logging.warning(message)
    logging.warning(bar)
    f.write(bar)
    f.write(cr)
    f.write(message)
    f.write(cr)
    f.write(bar)
    f.write(cr)
    f.close()

def write_line(message):
    # Set up file handler and carrige return
    f = open('lab_check.txt', 'a')
    cr = '\n'
    logging.warning(message)
    f.write(message)
    f.write(cr)
    f.close()
