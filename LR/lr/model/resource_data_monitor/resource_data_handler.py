# !/usr/bin/python
# Copyright 2011 Lockheed Martin

'''
Base couchdb threshold change handler class.

Created on August 31, 2011

@author: jpoyau
'''

#_PWD = path.abspath(path.dirname(__file__))

#import sys
##Add the config and lr module the sys path so that they can used.
#sys.path.append(path.abspath(path.join(_PWD, "../")))

import logging
import pprint
from lr.lib import BaseChangeHandler
from spec_models import ResourceDataFactory
import couchdb

_RESOURCE_DATA_TYPE = "resource_data"
_DOC_TYPE = "doc_type"
_DOC = "doc"

log = logging.getLogger(__name__)

class ResourceDataHandler(BaseChangeHandler):
    
    def __init__(self, specDefinitionFiles, destinationDBUrl, docType=_RESOURCE_DATA_TYPE):
        BaseChangeHandler.__init__(self)
        self._destinationDBUrl = destinationDBUrl
        self._specDefinitionFiles = specDefinitionFiles
        self._docType = docType

    def preRunSetup(self):
        self.ResourceDataModel = ResourceDataFactory(self._specDefinitionFiles, self._destinationDBUrl)
        self._destinationDB = couchdb.Database(self._destinationDBUrl)

    def _canHandle(self, change, database):
        if ((_DOC in change) and 
            (change[_DOC].get(_DOC_TYPE) ==self._docType)) :
                return True
        return False

    def _updateDistributableData(self, newDistributableData, distributableDocId):
        # Use the ResourceDataModel class to create an object that 
        # contains only a the resource_data spec data.
        currentDistributable = self._destinationDB[distributableDocId]
        temp = self.ResourceDataModel(currentDistributable)._specData
        del temp['node_timestamp']
         
        if newDistributableData != temp:
            currentDistributable.update(newDistributableData)
            log.debug("\n\nUpdate distribuatable doc:\n")
            log.debug("\n{0}\n\n".format(pprint.pformat(currentDistributable)))
            try:
                self._destinationDB.update([currentDistributable])
            except Exception as e:
                log.error("Failed to update existing distributable doc: {0}".format(
                                pprint.pformat(currentDistributable)))
                log.exception(e)
        
        
    def _addDistributableData(self, distributableData, distributableDocId):
        try:
            log.debug('Adding distributable doc %s...\n' % distributableDocId)
            self._destinationDB[distributableDocId] = distributableData
        except Exception as e:
            log.error("Cannot save distributable document %s\n" % distributableDocId)
            log.exception(e)

    def _handle(self, change, database):
      
        # Use the ResourceDataModel class to create an object that 
        # contains only a the resource_data spec data.
        distributableDoc = self.ResourceDataModel(change['doc'])._specData
        #remove the node timestamp
        del distributableDoc['node_timestamp']
        #change thet doc_type 
        distributableDoc['doc_type']='resource_data_distributable'
        distributableDocId= change['doc']['_id']+"-distributable"
       
        # Check to see if a corresponding distributatable document exist.
        # not create a new distribuation document without the 
        # node_timestamp and _id+distributable.
        if (distributableDocId in self._destinationDB) == False:
            self._addDistributableData(distributableDoc, distributableDocId)
        else:
            self._updateDistributableData(distributableDoc, distributableDocId)
