#!/usr/bin/pyton

#    Copyright 2011 Lockheed Martin

'''
Created on Mar 11, 2011

Base model class for learning registry data model

@author: jpoyau
'''


from base_model import createBaseModel
import logging

log = logging.getLogger(__name__)

def NetworkFactory(specDefinitionPath, databaseUrl):

    BaseModel = createBaseModel(specDefinitionPath, databaseUrl)
    
    class NetworkModel(BaseModel):
        
        _DESCRIPTION_DICT_KEYS =["network_id",
                                                        "network_description",
                                                        "network_name",
                                                        "network_key",
                                                        "network_admin_identity"
                                                    ]
        def __init__(self, data=None):
            super(NetworkModel,self).__init__(data)
            
    return NetworkModel
        
