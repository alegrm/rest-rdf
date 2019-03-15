# REST RDF

A simple Flask APP to implement the RESTful api, and Rdflib to handle RDF data. A single SPARQL query is used to retreive company data from the dataset and from the user-provided data. This query allows to avoid inserting undesired data to the dataset. 

## GET /company/<id:string>

Retreive data of a company.
* Consumes : text/turtle, application/rdf+xml
* Produces : text/turtle, application/rdf+xml

Example:

		curl -i http://127.0.0.1:5000/company/bbc

## PUT /company/<id:string>

Update (insert) triples to the graph with the specified identifier

* Consumes : text/turtle, application/rdf+xml

Example:

		curl -i http://127.0.0.1:5000/company/alibaba \
			--header "Content-Type: application/rdf+xml" \
			--request PUT \
			--data '<?xml version="1.0"?>
		<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
		xmlns:schema="http://schema.org/">
		<rdf:Description rdf:about="http://example.org/alibaba">
		  <rdf:type rdf:resource="http://schema.org/Organization"/>
		  <schema:name>Alibaba Group</schema:name>
		  <schema:founder rdf:resource="http://example.org/jack_ma"/>
		  <schema:url>https://www.alibabagroup.com</schema:url>
		</rdf:Description>
		</rdf:RDF>
		'


##GET /dataset

Retreive the complete dataset.

* Produces : text/turtle, application/rdf+xml

Example:
		curl -i http://127.0.0.1:5000/dataset --header "Accept:text/turtle"

# Useage

Use the following commands to install required packages, and to launch the server.

		pip install requirements.txt
		python3 

# Improvements

* Support concurrent access to the data store
* 
