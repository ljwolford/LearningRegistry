#!/usr/bin/pyton

#    Copyright 2011 Lockheed Martin

'''
Created on Mar 10, 2011

Base model class for learning registry data model

@author: jpoyau
'''


from base_model import createBaseModel
import logging

log = logging.getLogger(__name__)

def NodeFactory(specDefinitionPath, databaseUrl):

    BaseModel = createBaseModel(specDefinitionPath, databaseUrl)

    class NodeModel(BaseModel):
    
        #List of keys that are expected description is called on an object of this class.
        _DESCRIPTION_DICT_KEYS= ['active', 
                                                      'node_id',  
                                                      'node_description',
                                                      'node_name',
                                                      'node_key',
                                                      'node_admin_identity' ,
                                                      'open_connect_source',
                                                      'open_connect_dest',
                                                      'gateway_node']
    
        _NODE_POLICY_DESCRIPTION_DICT = ['sync_frequency',
                                                                      'deleted_data_policy',
                                                                      'accepted_version',
                                                                      'accepted_TOS',
                                                                      'accepts_anon',
                                                                      'accepts_unsigned',
                                                                      'validates_signature',
                                                                      'check_trust'
                                                                      ]
        def __init__(self, data=None):
            super(NodeModel, self).__init__(data)
        
        def _getDescriptionDict(self):
          
          #Call the BaseModel to get the first level description
            nodeDescriptionDict= NodeModel.__bases__[0]._getDescriptionDict(self) 
            if 'node_policy' in self._specData:
                #Get the only the keys that expected for node_policy
                validKeys = set(self.node_policy.keys()).intersection(self._NODE_POLICY_DESCRIPTION_DICT)
                nodeDescriptionDict["node_policy"] =  dict((k, self.node_policy[k]) for k in validKeys)
            return nodeDescriptionDict

    return NodeModel
