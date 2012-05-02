function(doc, req) {
	// !code lib/alignment.js
    var isGood = false;
    if (doc.doc_type === "resource_data" && doc.identity.owner) {
        isGood = true;
    }	
    return isGood;
}