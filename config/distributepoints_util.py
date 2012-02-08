import setup_utils as su


def setupDistributionConnections(currentList):
	
	newList = []

	flag = True
	while flag:
		print("\nCurrent distribution connections:")
		if len(currentList) > 0:
			for item in currentList:
				print item
		else:
			print("No distribution connections")		

		result = raw_input("\n[A]dd, [R]emove connections, [E]xit: ")

		if result == 'A' or result == 'a':
			for item in currentList:
				print item

			inputTargets = raw_input("Please enter any distrubtion targets you would like to add separated by a space: ")

			if inputTargets:
				newList = inputTargets.split(' ')

				for item in newList:
					currentList.append(item)
			
		elif result == 'R' or result == 'r':

			for index, item in enumerate(currentList):
				print '[' + str(index) +'] ' + item

			inputTarget = raw_input("Please enter the corresponding number to remove the distribution target:")

			if inputTarget:
				try:
					del currentList[int(inputTarget)]
				except Exception, e:
					print(e)
					print("Cannot delete specified connection")

		elif result == 'E' or result == 'e':
			flag = False
		else:
			continue
	
	return currentList	
	
def getExistingDistrubutionConnections(couchdbURL, dbName, nodeName):
    connFilter = nodeName + "_to_"
    connDocList = []

    try:
        connDocs = su.getDocFromExistingCouchDB(dbName, couchdbURL,allDocs=True)
        
        for connDoc in connDocs['rows']:
            if connFilter in connDoc['id']:
                connDocList.append(connDoc['id'])

    except Exception, e:
        print(e)
        print('Connection to Node database not established, using default distribution connections')        

    if not connDocList:
        return []
    else:    
        return getExistingDistrubtionURLs(couchdbURL, dbName, connDocList)    


def getExistingDistrubtionURLs(couchdbURL, dbName, connDocList):
    connUrlList = []

    for connDoc in connDocList:
        try:
            connURL = su.getDocFromExistingCouchDB(dbName, couchdbURL, connDoc)
            connUrlList.append(connURL['destination_node_url'])

        except Exception, e:
            print(e)
            print('Connection to Node database not established, using default distribution connection URLs')

    return connUrlList


'''
if __name__ == "__main__":
	import os
	import couchdb
	import ConfigParser


	scriptPath = os.path.dirname(os.path.abspath(__file__))
	_PYLONS_CONFIG =  os.path.join(scriptPath, '..', 'LR', 'development.ini')
	_config = ConfigParser.ConfigParser()
	_config.read(_PYLONS_CONFIG)

	_DEFAULT_COUCHDB_URL = _config.get("app:main", "couchdb.url")
	_NODE = _config.get("app:main", "couchdb.db.node")
	_NODE_DESCRIPTION = "node_description"
	_DEFAULT_ENDPOINT = _config.get("app:main", "node.endpoint.url")


	server =  couchdb.Server(_DEFAULT_COUCHDB_URL)
	existingNodeName = ""

	try:
		node_desc = getDocFromExistingCouchDB(_NODE, _DEFAULT_COUCHDB_URL, _NODE_DESCRIPTION)
		existingNodeName = node_desc['node_name']
	except Exception, e:
		raise e
	
	existingDistributionList = getExistingDistrubutionConnections(_DEFAULT_COUCHDB_URL, _NODE, existingNodeName)
	newDistributionList = setupDistributionConnections(existingDistributionList)
	publishNodeConnections(_DEFAULT_ENDPOINT, server, _NODE, existingNodeName, newDistributionList)
'''	