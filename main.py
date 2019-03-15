from flask import Flask, request, make_response
from flask_restful import Resource, Api, abort
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.plugins import sparql, parsers
from xml import sax
import os,tempfile


turtle_mediatype = 'text/turtle'
rdf_mediatype = 'application/rdf+xml'

supported_media = [ turtle_mediatype, rdf_mediatype ]
default_mediatype = turtle_mediatype

app = Flask(__name__)
api = Api(app)

local_file = "data.ttl"

companies_graph = Graph()

company_query = sparql.prepareQuery("""
    CONSTRUCT { 
        ?company <http://schema.org/name> ?name . 
        ?company a <http://schema.org/Organization> . 
        ?company <http://schema.org/subOrganization> ?subOrganization .
        ?company <http://schema.org/owner> ?owner .
        ?company <http://schema.org/founder> ?founder .
        ?company <http://schema.org/url> ?url .  
    } WHERE { 
        ?company <http://schema.org/name> ?name . 
        OPTIONAL { ?company a <http://schema.org/Organization> . }
        OPTIONAL { ?company <http://schema.org/subOrganization> ?subOrganization } .
        OPTIONAL { ?company <http://schema.org/owner> ?owner } .
        OPTIONAL { ?company <http://schema.org/founder> ?founder } .
        OPTIONAL { ?company <http://schema.org/url> ?url } .
    } """,
    initNs = { "schema": Namespace("http://schema.org") })


class Company(Resource):
        
    def put(self, company_id):

        if request.headers['Content-type'].lower() not in supported_media:
            abort(415, message="Unsupported medyatype, please provide" + " or ".join(supported_media))

        dataFormat = request.headers['Content-type'].lower()
        payload = request.data
        temporal_graph = Graph()

        try:
            temporal_graph.parse(data=payload, format=dataFormat)
        except (parsers.notation3.BadSyntax, sax._exceptions.SAXParseException) as e:
            abort(400, message=str(e))

        company = URIRef("http://example.org/" + company_id)
        result = temporal_graph.query(company_query, initBindings={'company': company})

        if len(result) == 0:
            abort(400, message="No triples provided for " + company)

        for s, p, o in result:
            companies_graph.add((s, p, o))

        companies_graph.serialize(destination=local_file, format="turtle")

        response = make_response(result.serialize(format=dataFormat), 201)
        response.headers['Content-type'] = turtle_mediatype
        return response

    def get(self, company_id):

        responseFormat = default_mediatype
        if request.headers['Accept'].lower() in supported_media:
            responseFormat = request.headers['Accept'].lower()
            print(responseFormat)

        print(responseFormat)

        company = URIRef("http://example.org/" + company_id)

        result = companies_graph.query(company_query, initBindings={'company': company})

        if len(result) == 0:
            abort(404, message="Company {} doesn't exist".format(company))
        else:            
            response = make_response(result.serialize(format=responseFormat), 200)
            response.headers['Content-type'] = responseFormat
            return response

api.add_resource(Company, '/company/<string:company_id>')

@app.route('/dataset', methods=['GET'])
def download():
    responseFormat = default_mediatype
    if request.headers['Accept'].lower() in supported_media:
        responseFormat = request.headers['Accept'].lower()
        print(responseFormat)

    response = make_response(companies_graph.serialize(format=responseFormat), 200)
    response.headers['Content-type'] = responseFormat
    return response


if __name__ == '__main__':
    companies_graph.parse(local_file, format="turtle")
    app.run(debug=True)

