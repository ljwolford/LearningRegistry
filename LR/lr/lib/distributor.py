#!/usr/bin/pyton

#    Copyright 2011 Lockheed Martin

'''
Created on Dec 12, 2011

Class to handle distribute/replication

@author: jpoyau


'''
import sys

def class Distributor(object):
    """Class the handles node distribution"""
    
    def __init__(self, sourceNode):
        self._validConnections = []
        self._invalidConnections = []
        self._getConnectionInfo(sourceNode.connections)
        
    def _getDistinationInfo(self, connection):
        # Make sure we only have one slash in the url path. More than one 
        #confuses pylons routing libary.
        destinationURL = urlparse.urljoin(connection.destination_node_url.strip(),
                                                                "destination")
        
        request = urllib2.Request(destinationURL)
        credential = sourceLRNode.getDistributeCredentialFor(destinationURL)
        
        if credential is not None:
            base64string = base64.encodestring('%s:%s' % (credential['username'],
                                                                    credential['password'])).replace("\n", "")
    
            request.add_header("Authorization", "Basic %s" % base64string)
        
        log.info("\n\nAccess destination node at: "+pprint.pformat(request.__dict__))
        return json.load(urllib2.urlopen(request))

        
    def _canDistributeTo(self, connection):
        
        if  not connection.active:
            return {self.__OK: False, 
                         'connection_id': connection.connection_id, 
                         self.__ERROR: 'Inactive connection'}
              
        result={self.__OK:True, 'connection_id': connection.connection_id }
        sourceNodeInfo = h.dictToObject(sourceNodeInfo)
        try:
            destinationNodeInfo = h.dictToObject(self._getDistinationInfo(connection)[self.__TARGET_NODE_INFO])
            result['destinationNodeInfo'] = destinationNodeInfo
            
            if ((sourceNodeInfo.gateway_node or destinationNodeInfo.gateway_node)  != connection.gateway_connection):
                result[self.__ERROR] = " 'gateway_connection' mismatch between nodes and connection data"
            
            elif ((sourceNodeInfo.community_id != destinationNodeInfo.community_id) and
                    ((not sourceNodeInfo.social_community) or (not destinationNodeInfo.social_community))):
                result[self.__ERROR] = 'cannot distribute across non social communities'
             
            elif ((sourceNodeInfo.network_id != destinationNodeInfo.network_id) and
                    ((not sourceNodeInfo.gateway_node)or(not destinationNodeInfo.gateway_node))):
                result[self.__ERROR] = 'cannot distribute across networks (or communities) unless gateway'
            
            elif ((sourceNodeInfo.gateway_node and destinationNodeInfo.gateway_node)
                    and (sourceNodeInfo.network_id == destinationNodeInfo.network_id)):
                result[self.__ERROR]  = 'gateway must only distribute across different networks'
    
            elif (sourceNodeInfo.gateway_node and not destinationNodeInfo.gateway_node):
                result[self.__ERROR]  = 'gateways can only distribute to gateways'
        except urllib2.URLError as ex:
            log.exception(ex)
            result[self.__ERROR] = "Cannot reach destination node.  "+str(ex.reason)
        except Exception as ex:
            log.exception(ex)
            result[self.__ERROR] = "Internal error. Cannot process destination node info"
        
        if result.has_key(self.__ERROR):
            result[self.__OK] = False
        
        return result
        
    def _buildDistributionList(self, connectionList):
        
        for connection  in connectionLlist:
            
    
