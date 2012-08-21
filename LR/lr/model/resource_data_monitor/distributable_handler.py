# !/usr/bin/python
# Copyright 2011 Lockheed Martin

'''
Base couchdb threshold change handler class.

Created on August 31, 2011

@author: jpoyau
'''
from os import path

#_PWD = path.abspath(path.dirname(__file__))

#import sys
##Add the config and lr module the sys path so that they can used.
#sys.path.append(path.abspath(path.join(_PWD, "../")))

from lr.lib.couch_change_monitor import BaseChangeHandler
import pprint
from spec_models import ResourceDataFactory
import logging
import couchdb

log = logging.getLogger(__name__)

_RESOURCE_DISTRIBUTABLE_TYPE = "resource_data_distributable"
_DOC_TYPE = "doc_type"
_DOC = "doc"

class DistributableHandler(BaseChangeHandler):
    def __init__(self, specDefinitionFiles, destinationDBUrl, docType=_RESOURCE_DISTRIBUTABLE_TYPE ):
        BaseChangeHandler.__init__(self)
        self._destinationDBUrl = destinationDBUrl
        self._specDefinitionFiles = specDefinitionFiles
        self._docType = docType

    def preRunSetup(self):
        self.ResourceDataModel = ResourceDataFactory(self._specDefinitionFiles, self._destinationDBUrl)
        self._destinationDB = couchdb.Database(self._destinationDBUrl)
      

    def _canHandle(self, change, database):
        if ((_DOC in change) and 
            (change[_DOC].get(_DOC_TYPE) == self._docType)) :
                return True
        return False
        
    def _getResourceDataDoc(self, docID, database):
        # There exist already a resource_data document for the distributable
        # get it and see if it needs to be updated.
        try:
            return  self.ResourceDataModel(database[docID])._specData
        except Exception as e:
            log.error("Cannot find existing resource_data doc for distributable: {0}\n".format(
                            docID))
            log.exception(e)
            return None
    
    def _updateResourceData(self, newResourceData, database):
        currentResourceData = self._getResourceDataDoc(newResourceData['doc_ID'], database)
        if currentResourceData == None:
            return 
            
        # Now delete the node_timestamp field on both document before comparing them.
        temp = {}
        temp.update(currentResourceData)
        del temp['node_timestamp']
        del newResourceData['node_timestamp']
        
        if temp != newResourceData:
            currentResourceData.update(newResourceData)
            try:
                log.debug("\nUpdate existing resource data from distributable\n")
                database.update([currentResourceData])
            except Exception as e:
                log.error("\n\nFailed to udpate existing resource_data doc:\n{0}".format(
                                pprint.pformat(currentResourceData)))
                log.exception(e)

    def _addResourceData(self, resourceDataCopy, database):
        # If corresponding resource_data type document is not already in the database
        # for the distributable document, create a local resource_data document and
        # add it the database
        try:
            log.debug("Adding new resource_data for distributable")
            database[resourceDataCopy['doc_ID']] = resourceDataCopy
        except Exception as e:
            log.error("\n\nCannot get current document:  {0}".format(
                            pprint.pformat(resourceDataCopy)))
            log.exception(e)
    
    def _handle(self, change, database):
        # The resource data copy is what the corresponding resource data document
        #  for this distributable document should look like.
        resourceDataCopy = self.ResourceDataModel(change['doc'])._specData
        resourceDataCopy['doc_type'] = 'resource_data'

        # Use the change monitor database as destination db if it is the same url
        # as the defined destinationDB so that everything stays in the same 
        # resource context when checking if the document is already in the database
        destinationDB = self._destinationDB
        if self._destinationDB.resource.url == database.resource.url:
            destinationDB = database

        # Add the corresponding resource data document to database 
        # if not already in the database.  Otherwise try to update. 
        if (resourceDataCopy['doc_ID'] in destinationDB) == False:
            self._addResourceData(resourceDataCopy, destinationDB)
        else:
            self._updateResourceData(resourceDataCopy, destinationDB)
