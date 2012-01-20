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

def NodeFilterFactory(specDefinitionPath, databaseUrl):
    
    BaseModel = createBaseModel(specDefinitionPath, databaseUrl)
    
    class NodeFilterModel(BaseModel):
        _DESCRIPTION_DICT_KEYS = ["filter_name",
                                                        "custom_filter",
                                                        "include_exclude",
                                                        "filter"
                                                        ]
        def __init__(self, data=None):
            super(NodeFilterModel,self).__init__(data)

    return NodeFilterModel
