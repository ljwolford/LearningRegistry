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

def NodeServiceFactory(specDefinitionPath, databaseUrl):
  
    BaseModel = createBaseModel(specDefinitionPath, databaseUrl)

    class NodeServiceModel(BaseModel):
        def __init__(self, data=None):
            super(NodeServiceModel,self).__init__(data)

    return NodeServiceModel
