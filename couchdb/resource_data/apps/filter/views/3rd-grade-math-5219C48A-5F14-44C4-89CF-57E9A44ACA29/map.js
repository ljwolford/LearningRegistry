function(doc) {
	if (doc.doc_type && doc.doc_type == "resource_data" &&
	    doc.doc_version && doc.doc_version == "0.10.0" &&
            doc.resource_data_type && doc.resource_data_type == "metadata" &&
            doc.submitter && doc.submitter == "NSDL 2 LR Data Pump" &&
	    doc.payload_placement && doc.payload_placement == "inline" &&
            doc.payload_schema && doc.keys && doc.create_timestamp) {
		
		var pass = false;
		for (var i = 0; i < doc.payload_schema.length; i++) {
			if (doc.payload_schema[i] == "NSDL DC 1.02.020") {
				pass = true;
				break;
			}
		}

		if (pass == true) {
			var terms = [ "Middle School", "Arithmetic"];
			var found = {};
			var count = 0;
			for (var i = 0; i < doc.keys.length; i++) {
				for (var t=0; t<terms.length; t++) {
					if (terms[t] == doc.keys[i] && !found[terms[t]]) {
						count ++;
						found[terms[t]] = true;
					}
				}
				if (count >= terms.length) {
					emit(doc.create_timestamp, doc.doc_ID);
					break;
				}

			}
			
		}

	}  
}
