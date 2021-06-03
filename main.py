from fastapi import FastAPI
import uvicorn

from SPARQLWrapper import SPARQLWrapper, JSON

app = FastAPI()
query = "atal bihari vajpayee"
query = query.title().replace(" ", "_")


@app.get("/")
def read_root():
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')

    # fetch from front end

    # sparQL query
    sparql.setQuery(f'''
    SELECT ?name ?comment ?image 
    WHERE {{ dbr:{query} rdfs:label ?name;
                        rdfs:comment ?comment.
                        
        
            FILTER (lang(?name) = 'en')
            FILTER (lang(?comment) = 'en')
            }}''')

    sparql.setReturnFormat(JSON)
    ques = sparql.query().convert()

    result = ques['results']['bindings'][0]
    name, comment = result['name']['value'], result['comment']['value']

    return {"name": [name], "About": [comment]}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8081, debug=True)
