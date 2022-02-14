import json
import os

class Cache():
    def __init__(self, tag):
        self.tag = tag

        if not os.path.exists('./cache'):
            os.mkdir('cache')
            
        self.path = f'./cache/{self.tag}'

    def create_cache_file(self):
        # create cache directory and file if one doesn't exist
        if not os.path.exists(self.path):
            f = open(self.path, 'x')
            f.close()

    def search(self, url, params):
        # url - url associated with entry being searched
        # params - params associated with entry being searched
        # search for entry in cache that matches given url and params
        with open(self.path, 'r') as f:
            for line in f:
                obj = json.loads(line)
                if url == obj["url"] and params == obj["params"]:
                    return obj["data"]

            return False

    def write(self, url, params, data):
        # url - url of endpoint being queried
        # params - params url was queried with
        # data - data returned from request
        # write an object to cache
        # TODO: make sure no error messages get written to cache (or
        # anything that isn't actual data)

        with open(self.path, 'a') as f:
            d = {'url' : url,
                'params' : params,
                'data' : data}

            f.write(json.dumps(d) + '\n')
