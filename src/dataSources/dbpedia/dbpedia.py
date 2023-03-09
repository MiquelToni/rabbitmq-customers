# SparQL class extension
# Prefixes and Class based from https://github.com/ejrav/pydbpedia
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlEndpoint(object):

    def __init__(self, endpoint, prefixes={}):
        self.sparql = SPARQLWrapper(endpoint)
        self.prefixes = {
            "dbo": "http://dbpedia.org/ontology/",
            "owl": "http://www.w3.org/2002/07/owl#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dbpedia2": "http://dbpedia.org/property/",
            "dbpedia": "http://dbpedia.org/",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "yago": "http://dbpedia.org/class/yago/",
            "schema": "https://schema.org/",
            "wikidata": "https://www.wikidata.org/wiki",
        }
        self.prefixes.update(prefixes)
        self.sparql.setReturnFormat(JSON)

    def query(self, q):
        lines = ["PREFIX %s: <%s>" % (k, r) for k, r in self.prefixes.items()]
        lines.extend(q.split("\n"))
        query = "\n".join(lines)
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return results["results"]["bindings"]


class DBpediaEndpoint(SparqlEndpoint):
    def __init__(self, endpoint, prefixes={}):
        super(DBpediaEndpoint, self).__init__(endpoint, prefixes)


if __name__ == "__main__":
    s = DBpediaEndpoint(endpoint="http://dbpedia.org/sparql")
    result = s.query('''
SELECT ?x, ?name
WHERE {
    { 
        ?x a dbo:Company ;
        dbp:name ?name ;
        dbo:abstract ?abstract

    } UNION { 
        ?x a dbo:Organisation ;
        dbp:name ?name ;
        dbo:abstract ?abstract
    }
    UNION { 
        ?x a schema:Organization ;
        dbp:name ?name ;
        dbo:abstract ?abstract
    }
    UNION { 
        ?x a wikidata:Q43229 ;
        dbp:name ?name ;
        dbo:abstract ?abstract
    }
    UNION { 
        ?x a wikidata:Q4830453 ;
        dbp:name ?name ;
        dbo:abstract ?abstract
    } .
        
    FILTER (CONTAINS(LCASE(STR(?abstract)), "rabbitmq")) .
}
LIMIT 500
    ''')
    print(len(result), result)
