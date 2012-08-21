# !/usr/bin/python
# Copyright 2011 Lockheed Martin

'''
Base couchdb threshold change handler class.

Created on August 18, 2011

@author: jpoyau
'''

import pprint
import logging
import atexit
from pylons import config
import os
import signal
import subprocess

log = logging.getLogger(__name__)


def startMonitor():
    command = '(cd {0}; python monitor_dbchange.py  --c {1})'.format(
                                    os.path.abspath(os.path.dirname(__file__)),
                                    os.path.abspath(config['__file__']))
                                    
    #Create a process group name as so that the shell and all its process
    # are terminated when stop is called.
    monitorProcess = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    return monitorProcess

def monitorResourceDataChanges(): 
    
    monitorProcess = startMonitor()

    def atExitHandler():
        os.killpg(monitorProcess.pid, signal.SIGTERM)
        log.debug("Change monitor process is halted {0}\n\n")

    atexit.register(atExitHandler)
