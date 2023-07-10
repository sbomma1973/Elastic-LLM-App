from elasticsearch import Elasticsearch
import requests
from datetime import datetime
import json
import yaml
def es_connect(cloud_id,username,password):
    es = Elasticsearch(cloud_id=cloud_id, http_auth=(username, password))
    print (es.info())
    return es
def read_from_file():
    with open('config.yml') as f:
        data = yaml.load (f, Loader=yaml.FullLoader)
        return data
def search (query_txt):
    data = read_from_file()
    username = data['username']
    password = data['password']
    cloud_id1 = data['cloud_id']
    index_name = data['index_name']
    #print ( username, password, cloud_id1, index_name)


    es = es_connect(cloud_id1, username, password)
    query = {
             "text_expansion": {
                                    "ml.inference.body_content_expanded.predicted_value": {
                                    "model_text": query_txt ,
                                    "model_id": ".elser_model_1",
                                    "boost": 3
                                }
                }
          }
    index=index_name
    fields = ["body_content","url","title"]

    resp = es.search(index=index_name,fields=fields, query=query, size=3, source=False)

    print (resp)
    #for hit in resp['hits']['hits']:
     #   print("q" % hit["_source"])
    body = resp['hits']['hits'][0]['fields']['body_content'][0]
    url = resp['hits']['hits'][0]['fields']['url'][0]

    #print ("body>"% body)
    print ("body>>",body)
    print ("url>>",url)

if __name__ == '__main__':
    print("Hello")

    search('bratwurst')

