# !/usr/bin/python
# Copyright 2011 Lockheed Martin

'''
Base couchdb threshold change handler class.

Created on August 18, 2011

@author: jpoyau
'''
from os import path

_PWD = path.abspath(path.dirname(__file__))

import sys
#Add the config and lr module the sys path so that they can used.
sys.path.append(path.abspath(path.join(_PWD,"../../config")))
sys.path.append(path.abspath(path.join(_PWD, "../../../")))

import pprint
import logging
from lr.lib import MonitorChanges
import atexit
from lr.model import ResourceDataModel
from distributable_handler import DistributableHandler
from resource_data_handler import ResourceDataHandler
from update_views_handler import  UpdateViewsHandler
from distribute_threshold_handler import DistributeThresholdHandler
from track_last_sequence import TrackLastSequence


log = logging.getLogger(__name__)

_RESOURCE_DATA_CHANGE_ID =  "_local/Last_Processed_Change_Sequence"


def _getLastSavedSequence():
    lastSavedSequence = -1
    if _RESOURCE_DATA_CHANGE_ID in ResourceDataModel._defaultDB:
        lastSavedSequence=ResourceDataModel._defaultDB[_RESOURCE_DATA_CHANGE_ID][TrackLastSequence._LAST_CHANGE_SEQ]
    return lastSavedSequence

    
def monitorResourceDataChanges(config['app_conf'], handlers): 
    options = {'since':_getLastSavedSequence()}
    log.debug("\n\n-----"+pprint.pformat(options)+"------\n\n")

    changeMonitor = MonitorChanges(config['app_conf']['couchdb.url'], 
                                                            config['app_conf']['couchdb.db.resourcedata'],
                                                            _RESOURCE_DATA_CHANGE_HANDLERS,
                                                            options)
    changeMonitor.start()
    
    #changeMonitor.start(threading.current_thread())
    def atExitHandler():
        changeMonitor.terminate()
        log.debug("Last change {0}\n\n".format(changeMonitor._lastChangeSequence))

    atexit.register(atExitHandler)
    
if __name__ == '__main__':

    import lr.config.environment as e
    
    config = e.load_environment(e.global_conf, e.app_conf)
    config['app_conf'] = config['app_conf']
    
    handlers =[
        rackLastSequence(_RESOURCE_DATA_CHANGE_ID),
        DistributableHandler(),
        ResourceDataHandler(),
        UpdateViewsHandler(config['app_conf']['couchdb.threshold.viewupdate']),
        DistributeThresholdHandler(config['app_conf']['couchdb.threshold.distributes'])
    ]

    
    monitorResourceDataChanges(config['app_conf'], handlers)
    
