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
sys.path.append(path.abspath(path.join(_PWD, "../")))

import pprint
import logging
from lr.lib import MonitorChanges
import atexit
import ConfigParser
from spec_models import ResourceDataFactory
from distributable_handler import DistributableHandler
from resource_data_handler import ResourceDataHandler
from update_views_handler import  UpdateViewsHandler
from distribute_threshold_handler import DistributeThresholdHandler
from track_last_sequence import TrackLastSequence
import couchdb
from datetime import timedelta

log = logging.getLogger(__name__)

_RESOURCE_DATA_CHANGE_ID =  "_local/Last_Processed_Change_Sequence" 

_config = ConfigParser.ConfigParser()
 

def _getLastSavedSequence(databaseUrl):
    lastSavedSequence = -1
    db = couchdb.Database(databaseUrl)
    if _RESOURCE_DATA_CHANGE_ID in db:
        lastSavedSequence=db[_RESOURCE_DATA_CHANGE_ID][TrackLastSequence._LAST_CHANGE_SEQ]
    return lastSavedSequence

    
def monitorResourceDataChanges(handlers, databaseUrl, lastSeq): 
    options = {'since': lastSeq}
    log.debug("\n\n-----"+pprint.pformat(options)+"------\n\n")

    changeMonitor = MonitorChanges(databaseUrl, handlers, options)
    changeMonitor.start()
    changeMonitor.join()
    #changeMonitor.start(threading.current_thread())


if __name__ == '__main__':
    from optparse import OptionParser    
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="configPath", 
                      help="The full path of the pylons config file.",  metavar="FILE")
                    
    (options, args) = parser.parse_args()
    
    config = ConfigParser.ConfigParser()
    config.read(options.configPath)
        
    #Set logging level to same as the lr log level
    logging.basicConfig(level=config.get('logger_routes', 'level'))
    
    log.debug("Using pylons configuration files '{0}'".format(options.configPath))
    
    #Set here to the location of the configuration directory.
    config.set('DEFAULT', 'here', path.abspath(path.dirname(options.configPath)))

    
    ResourceDataModel = ResourceDataFactory(config.get("app:main", "spec.models.resource_data"),
                                                                           config.get("app:main", "couchdb.db.resourcedata"))

    handlers =[
        TrackLastSequence(_RESOURCE_DATA_CHANGE_ID),
        
        DistributableHandler(config.get("app:main", "spec.models.resource_data"),
                                          config.get("app:main", "couchdb.db.resourcedata")),
                                          
        ResourceDataHandler(config.get("app:main", "spec.models.resource_data"),
                                            config.get("app:main", "couchdb.db.resourcedata")),

        UpdateViewsHandler(config.get('app:main', 'couchdb.threshold.viewupdate')),
        
        DistributeThresholdHandler(config.get('app:main', 'couchdb.db.resourcedata'),
                                                     config.get('app:main', 'distribute.threshold.count'),
                                                     timedelta(seconds=int(config.get('app:main', 'distribute.threshold.time'))))
    ]
    monitorOpts = {'since': _getLastSavedSequence(config.get('app:main', 'couchdb.db.resourcedata'))}
    changeMonitor = MonitorChanges(config.get('app:main', 'couchdb.db.resourcedata'), handlers, monitorOpts)
    
    def atExitHandler():
        changeMonitor.terminate()
        log.debug("Last change {0}\n\n".format(changeMonitor._lastChangeSequence))

    atexit.register(atExitHandler)
    log.debug("\n\n-----------Start database monintoring-------------------\n\n")
    changeMonitor.start()
    changeMonitor.join()

