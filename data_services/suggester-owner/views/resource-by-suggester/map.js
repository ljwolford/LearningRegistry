function(doc) {
    // !code lib/alignment.js
    try {
    	if (doc.doc_type == "resource_data" && doc.resource_data && doc.resource_locator && doc.node_timestamp) {
        	var nodeTimestamp = convertDateToSeconds(doc);
        	var owner = "";
            if(doc.identity.owner != ""){
                owner = doc.identity.owner
            }
        	emit([owner, doc.resource_locator], nodeTimestamp);
    	}
       
    } catch (error) {
            log("error:"+error);
    }
}

