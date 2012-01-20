#!/usr/bin/pyton

#    Copyright 2011 Lockheed Martin

'''
Created on Mar 17, 2011

Base model class for learning registry data model

@author: jpoyau
'''


from base_model import createBaseModel
import logging

log = logging.getLogger(__name__)

def NetworkPolicyFactory(specDefinitionPath, databaseUrl):

    BaseModel = createBaseModel(specDefinitionPath, databaseUrl)
    
    class NetworkPolicyModel(BaseModel):
        _DESCRIPTION_DICT_KEYS = [ 'policy_id',
                                                         'policy_version',
                                                         'network_id']
                                                         
        def __init__(self, data=None):
            super(NetworkPolicyModel, self).__init__(data)

    return NetworkPolicyModel
