function(doc) {
    // !code lib/alignment.js
    try {
        if (doc.doc_type === "resource_data" && doc.resource_locator && doc.node_timestamp && doc.identity.owner) {
            var nodeTimestamp = convertDateToSeconds(doc);
            var owner = "";
            if(doc.identity.owner != ""){
                owner = doc.identity.owner
            }
            emit([doc.resource_locator, owner], nodeTimestamp);
        }   
    } catch (error) {
            log("error:"+error);
    }
 }