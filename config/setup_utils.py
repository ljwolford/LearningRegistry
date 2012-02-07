'''
Created on Aug 16, 2011

@author: jklo
'''
import couchdb 
import sys
import traceback
from uuid import uuid4
import lrnodetemplate as t
from pprint import pprint
import urlparse
import ConfigParser
import os
import urllib2
import json
#from connections_util import setupDistributionConnections
import distributepoints_util as dp
 

scriptPath = os.path.dirname(os.path.abspath(__file__))
_PYLONS_CONFIG =  os.path.join(scriptPath, '..', 'LR', 'development.ini')
_config = ConfigParser.ConfigParser()
_config.read(_PYLONS_CONFIG)

#Default url to the couchdb server.
_DEFAULT_COUCHDB_URL = _config.get("app:main", "couchdb.url")
_NODE = _config.get("app:main", "couchdb.db.node")
_NODE_DESCRIPTION = "node_description"
_DEFAULT_ENDPOINT = _config.get("app:main", "node.endpoint.url")
_DEFAULT_DISTRIBUTE_RESOURCE_DATA_URL = _config.get("app:main", "lr.distribute_resource_data_url")


def publishService(nodeUrl, server, dbname, serviceType, serviceName):
    service = {}
    service.update(t.service_description)
    service['service_type'] =serviceType
    service['service_id'] = uuid4().hex
#    service['service_name'] = serviceName+" service"
    service['service_name'] = serviceName
    service["service_endpoint"] = urlparse.urljoin(nodeUrl, serviceName)
    service['service_description']= "{0} {1} service".format(serviceType, serviceName)
    PublishDoc(server, dbname,  "{0}:{1} service".format(serviceType, serviceName), service)

def CreateDB(couchServer = _DEFAULT_COUCHDB_URL,  dblist=[], deleteDB=False):
    '''Creates a DB in Couch based upon config'''
    for db in dblist:
        if deleteDB:
            try:
                del couchServer[db]
            except couchdb.http.ResourceNotFound as rnf:
                print("DB '{0}' doesn't exist on '{1}', creating".format(db, couchServer))
        else:
            try:
                existingDB = couchServer[db]
                print("Using existing DB '{0}' on '{1}'\n".format(db, couchServer))
                continue
            except:
                pass
        try:
            couchServer.create(db)
            print("Created DB '{0}' on '{1}'\n".format(db, couchServer))
        except Exception as e:
            print("Exception while creating database: {0}\n".format(e) )


def PublishDoc(couchServer, dbname, name, doc_data):
    try:
        #delete existing document.
        db = couchServer[dbname]
        if "_rev" in doc_data:
            del doc_data["_rev"]
       
        try:
            del db[name]
        except:
            pass
        db[name] = doc_data
        print("Added config document '{0}' to '{1}'".format(name, dbname))
    except  Exception as ex:
        print("Exception when add config document:\n")
        exc_type, exc_value, exc_tb = sys.exc_info()
        pprint(traceback.format_exception(exc_type, exc_value, exc_tb))
    

def testCouchServer(serverURL):
    try:
        couchServer =  couchdb.Server(url=serverURL)
        # Try to get the server configuration to ensure the the server is up and
        # and running. There may be a better way of doing that.
        couchServer.config()
    except Exception as e:
        print(e)
        print("Cannot connect to couchDB server '{0}'\n".format(serverURL))
        return False
    return True

def getInput(question, defaultInput=None,  validateFunc=None):
    ques = question+':  '
    if defaultInput is not None:
            ques = question+' [{0}]:  '.format(defaultInput)

    while True:
        userInput = raw_input(ques)
        inputLen =  len(userInput.strip())
        if inputLen == 0:
            if defaultInput is not None:
                userInput = defaultInput
            else:
                continue

        if validateFunc is not None and validateFunc(userInput) == False:
            continue
           
        return userInput


def isURL(userInput):
    import re
    
    return re.match("^https?://[^/]+", userInput.lower()) is not None

YES = ['t', 'true', 'yes', 'y']
NO = ['f', 'false', 'no', 'n']

def isBoolean(userInput):
    if userInput.lower() in YES or userInput.lower in NO:
        return True

def isInt(userInput):
    try:
        int(userInput)
        return True
    except ValueError:
        return False

def canEditDistributeConnections(userInput):
    if userInput == 'Edit' or userInput == 'edit':
        return True
    else:
        inputListValues = userInput.split(' ')
        return inputListValues[1:] == defaultNodeDescriptionValues['_DEFAULT_CONNECTIONS'][1:]


def getDocFromExistingCouchDB(dbName, couchdbURL=_DEFAULT_COUCHDB_URL, docID='', allDocs=False):
    resp = {}

    print('in getDocFromExistingCouchDB')
    if allDocs:
        path = '/'.join([dbName,"_all_docs"])
    else:
        path = '/'.join([dbName, urllib2.quote(docID,'')])

    URI = couchdbURL + path
    print (URI)
    try:
        req = urllib2.Request(URI)
        resp = json.loads(urllib2.urlopen(req).read())
    except Exception, e:
        print e
        print("Could not establish couchDB connection")

    return resp    

def getNodeDescriptionValues(couchdbURL, dbName, docID, endpointURL):
    nodeDescriptionValues = {'_DEFAULT_NODE_NAME' : "Node@" + endpointURL,
                             '_DEFAULT_NODE_ADMIN_IDENTITY' : "admin@learningregistry.org",  
                             '_DEFAULT_NODE_DESCRIPTION' : "Node@" + endpointURL,   
                             '_DEFAULT_GATEWAY_NODE' : "F",
                             '_DEFAULT_OPEN_CONNECT_SOURCE' : "T",   
                             '_DEFAULT_OPEN_CONNECT_DEST' : "T",
                            }
    
    try:
        node_desc = getDocFromExistingCouchDB(dbName, couchdbURL, docID)
        
        nodeDescriptionValues['_DEFAULT_NODE_NAME'] = node_desc['node_name']
        nodeDescriptionValues['_DEFAULT_NODE_ADMIN_IDENTITY'] = node_desc['node_admin_identity']
        nodeDescriptionValues['_DEFAULT_NODE_DESCRIPTION'] = node_desc['node_description']
        nodeDescriptionValues['_DEFAULT_GATEWAY_NODE'] = str(node_desc['gateway_node'])[:1]
        nodeDescriptionValues['_DEFAULT_OPEN_CONNECT_SOURCE'] = str(node_desc['open_connect_source'])[:1]
        nodeDescriptionValues['_DEFAULT_OPEN_CONNECT_DEST'] = str(node_desc['open_connect_dest'])[:1]
            
    except Exception, e:
        print(e)
        print('Connection to Node database not established, using default setup values')

    return nodeDescriptionValues



def getSetupInfo():

    '''Set the node values the user will be prompted with'''
    defaultNodeDescriptionValues = getNodeDescriptionValues(_DEFAULT_COUCHDB_URL, _NODE, _NODE_DESCRIPTION, _DEFAULT_ENDPOINT) 
    defaultNodeDescriptionValues['_DEFAULT_CONNECTIONS'] =  dp.getExistingDistrubutionConnections(_DEFAULT_COUCHDB_URL,_NODE,defaultNodeDescriptionValues['_DEFAULT_NODE_NAME'])   


    """Get the user node info"""
    nodeSetup = {}
    
    nodeUrl = getInput("\nEnter the node service endpoint URL", 
                                            _DEFAULT_ENDPOINT, isURL)
    nodeSetup['nodeUrl'] = nodeUrl
    

    couchDBUrl  = getInput("Enter your couchDB server URL",
                                            _DEFAULT_COUCHDB_URL, testCouchServer)
    nodeSetup['couchDBUrl'] = couchDBUrl

    
    nodeName = getInput("Enter your node name", 
                                            defaultNodeDescriptionValues['_DEFAULT_NODE_NAME'])
    nodeSetup['node_name'] = nodeName

    
    nodeDescription = getInput("Enter your node description", 
                                            defaultNodeDescriptionValues['_DEFAULT_NODE_DESCRIPTION'])
    nodeSetup['node_description'] = nodeDescription


    adminUrl = getInput("Enter node admin indentity",
                                            defaultNodeDescriptionValues['_DEFAULT_NODE_ADMIN_IDENTITY'])
    nodeSetup['node_admin_identity'] = adminUrl


    manageDistributeTargets = getInput("Would you like to edit your distribution URLs?\nInput 'Edit' " +
                                            "to edit targets, or just hit Enter to keep existing targets", 
                                            ' '.join(map(str, defaultNodeDescriptionValues['_DEFAULT_CONNECTIONS'])),canEditDistributeConnections)
    
    if not (manageDistributeTargets == 'Edit' or manageDistributeTargets == 'edit') :
        nodeSetup['connections'] = defaultNodeDescriptionValues['_DEFAULT_CONNECTIONS']
    else:
        nodeSetup['connections'] = dp.setupDistributionConnections(defaultNodeDescriptionValues['_DEFAULT_CONNECTIONS'])

    
    isGatewayNode = getInput('\nIs the node a gateway node (T/F)', 
                                            defaultNodeDescriptionValues['_DEFAULT_GATEWAY_NODE'])
    nodeSetup['gateway_node'] = (isGatewayNode == 'T' or isGatewayNode =='t')

    
    isNodeOpen = getInput('Is the node "open" (T/F)', 
                                            defaultNodeDescriptionValues['_DEFAULT_OPEN_CONNECT_SOURCE'])
    nodeSetup['open_connect_source'] = (isNodeOpen == 'T' or isNodeOpen == 't')


    nodeSetup['distributeResourceDataUrl'] = getInput("\nEnter distribute/replication "+
                        "resource_data destination URL. This is the resource_data URL that another node couchdb "+
                        "will use to replicate/distribute to this node", 
                                            _DEFAULT_DISTRIBUTE_RESOURCE_DATA_URL)
    

    isDistributeDest = getInput("\nDoes the node want to be the destination for replication (T/F)", 
                                            defaultNodeDescriptionValues['_DEFAULT_OPEN_CONNECT_DEST'])
    nodeSetup['open_connect_dest'] = (isDistributeDest == 'T' or isDistributeDest == 't')

    return nodeSetup
