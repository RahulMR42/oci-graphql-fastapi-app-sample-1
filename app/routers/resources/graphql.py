import json
import requests

class graphql:
    def __init__(self,url):
        self.url = url

    def query(self,query):
        try:
            query_result = requests.post(self.url,json={"query": query})
            return query_result.json()
        except Exception as error:
            print(str(error))

    def mutation(self,mutation):
        try:
            mutation_result = requests.post(self.url,json={"query": mutation})
            return mutation_result.json()
        except Exception as error:
               print(str(error))





