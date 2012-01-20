#    Copyright 2011 Lockheed Martin

'''
Created on Jan  19, 2012

Base model class for learning registry data model

@author: jpoyau
'''

from spec_models import *
from pylons import config


CommunityModel = CommunityFactory(config['app_conf']['spec.models.community_description'],
                                                                config['app_conf']['couchdb.db.community'])

ResourceDataModel = ResourceDataFactory(config['app_conf']['spec.models.resource_data'],
                                                                       config['app_conf']['couchdb.db.resourcedata'])
                                                                       
NetworkModel = NetworkFactory(config['app_conf']['spec.models.network_description'],
                                                     config['app_conf']['couchdb.db.network'])
                                                     
NetworkPolicyModel = NetworkFactory(config['app_conf']['spec.models.network_policy_description'],
                                                              config['app_conf']['couchdb.db.network'])

NodeModel = NodeFactory(config['app_conf']['spec.models.node_description'],
                                            config['app_conf']['couchdb.db.node'])

NodeFilterModel = NodeFilterFactory(config['app_conf']['spec.models.filter_description'],
                                                            config['app_conf']['couchdb.db.node'])

NodeConnectivityModel = NodeConnectivityFactory(config['app_conf']['spec.models.node_connectivity_description'],
                                                                                    config['app_conf']['couchdb.db.node'])

NodeServiceModel = NodeServiceFactory(config['app_conf']['spec.models.node_service_description'],
                                                                     config['app_conf']['couchdb.db.node'])

NodeStatusModel = NodeStatusFactory(config['app_conf']['spec.models.status_description'],
                                                                config['app_conf']['couchdb.db.node'])


__all__ = [
            'CommunityModel',
            'ResourceDataModel',
            'NetworkModel',
            'NetworkPolicyModel',
            'NodeModel',
            'NodeFilterModel',
            'NodeConnectivityModel',
            'NodeServiceModel',
            'NodeStatusModel'
    ]
