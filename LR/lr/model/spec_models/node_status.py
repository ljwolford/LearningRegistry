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

def NodeStatusFactory(specDefinitionPath, databaseUrl):
    
    BaseModel = createBaseModel(specDefinitionPath, databaseUrl)
    
    class NodeStatusModel(BaseModel):
    
        def __init__(self, data=None):
            super(NodeStatusModel, self).__init__(data)

    return NodeStatusModel
