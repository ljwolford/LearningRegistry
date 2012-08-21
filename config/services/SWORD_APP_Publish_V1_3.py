'''
Created on Oct16, 2011

@author: wegrata
'''
from service_template import ServiceTemplate
from setup_utils import getInput, PublishDoc, isBoolean, YES, isInt
import pystache, uuid
import json



def install(databaseUrl, setupInfo):
    custom_opts = {}
    active = getInput("Enable SWORD Service?", "T", isBoolean)
    custom_opts["active"] = active.lower() in YES

    custom_opts["node_endpoint"] = setupInfo["nodeUrl"]
    custom_opts["service_id"] = uuid.uuid4().hex
    
    return __BasicSwordServiceTemplate().install(databaseUrl, custom_opts)


class __BasicSwordServiceTemplate(ServiceTemplate):
    def __init__(self):
        ServiceTemplate.__init__(self)    
        self.service_data_template = '''{
        }'''    
    
    def _optsoverride(self):
        opts = {
            "active": "false",
            "service_type": "publish",
            "service_name": "SWORD APP Publish V1.3",
            "service_version": "0.23.0",
            "service_endpoint": "/swordservice",
            "service_key": "false", 
            "service_https": "false",
            "doc_limit": None ,
            "msg_size_limit": None
        }
        return opts
        
if __name__ == "__main__":
    import couchdb
    
    nodeSetup = {
                 'couchDBUrl': "http://localhost:5984",
                 'nodeUrl': "http://test.example.com"
    }
    
    def doesNotEndInSlash(input=None):
        return input is not None and input[-1] != "/"
    
    def notExample(input=None):
        return input is not None and input != nodeSetup["nodeUrl"]

    nodeSetup["couchDBUrl"] = getInput("Enter the CouchDB URL:", nodeSetup["couchDBUrl"], doesNotEndInSlash)
    nodeSetup["nodeUrl"] = getInput("Enter the public URL of the LR Node", nodeSetup["nodeUrl"], notExample)
    
    server =  couchdb.Server(url= nodeSetup['couchDBUrl'])
    install(server, "node", nodeSetup)
    
