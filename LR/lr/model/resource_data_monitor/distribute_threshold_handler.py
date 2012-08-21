# !/usr/bin/python
# Copyright 2011 Lockheed Martin

'''
Base couchdb threshold change handler class.

Created on August 31, 2011

@author: jpoyau
'''
import urllib2
import pprint
from datetime import timedelta
from lr.lib.couch_change_monitor import BaseChangeThresholdHandler
import logging
import json


log = logging.getLogger(__name__)

class DistributeThresholdHandler(BaseChangeThresholdHandler):
    _DOC_TYPE = "doc_type"
    _DOC = "doc"
    _HEADERS = {'Content-Type':'application/json; charset=utf-8'}
    
    def __init__(self, distributeUrl, countThreshold,  timeThreshold=timedelta.max,  docType="resource_data"):
        
        BaseChangeThresholdHandler.__init__(self, countThreshold, timeThreshold)
        self._distributeUrl = distributeUrl
        self._docType = docType
        
    def _canHandle(self, change, database):
        if ((self._DOC in change) and 
            (change[self._DOC].get(self._DOC_TYPE) ==self._docType)) :
                return True
        return False
        
    def _handle(self, change, database):
        log.debug('start distribute')
        request = urllib2.Request(self._distributeUrl, None, self._HEADERS)
        request.get_method = lambda : "POST"
        log.debug(pprint.pformat(request))
        response = urllib2.urlopen(request) 
        log.debug('end distribute') 
    
