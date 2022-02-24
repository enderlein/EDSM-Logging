import json
import os

class Cache():
    def __init__(self, tag):
        self.tag = tag 
        self.path = f'./cache/{self.tag}'

        self.create_cache_file()

    def create_cache_file(self):
        # create cache directory and file if one doesn't exist
        if not os.path.exists('./cache'):
            os.mkdir('cache')

        if not os.path.exists(self.path):
            f = open(self.path, 'x')
            f.close()

    def search(self, *args, **kwargs):
        # url - url of endpoint associated with entry being searched
        # params - params associated with entry being searched
        # searches for entry in cache that matches given url and params
        with open(self.path, 'r') as f:
            for line in f:
                obj = json.loads(line)
                if args == obj["args"] and kwargs == obj["kwargs"]:
                    return obj["data"]

            return False

    def write(self, data, *args, **kwargs):
        # url - url of endpoint being queried
        # params - params url was queried with
        # data - data returned from request
        # write an object to cache
        # TODO: make sure no error messages get written to cache (or
        # anything that isn't actual data)

        with open(self.path, 'a') as f:
            d = {'args' : args,
                'kwargs' : kwargs,
                'data' : data}

            f.write(json.dumps(d) + '\n')

def cacheable(func):
    def wrapper(*args, **kwargs):
        cache = kwargs['cache']
        if cache:
            c = Cache(func.__name__)
            cache_search = c.search(args, kwargs)

            if cache_search:
                return cache_search

        elif not cache:
            func(*args, **kwargs)

    return wrapper
