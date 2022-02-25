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

    def search(self, args, kwargs):
        # searches for entry in cache that matches given args and kwargs

        # popping 'cache' flag here because it's never stored
        if 'cache' in kwargs:
            kwargs.pop('cache')

        with open(self.path, 'r') as f:
            for line in f:
                obj = json.loads(line)
                if list(args) == obj["args"] and kwargs == obj["kwargs"]:
                    return obj["data"]

            return False

    def write(self, data, args, kwargs):
        # write an object to cache
        # TODO: make sure no error messages get written to cache (or
        # anything that isn't actual data)
        # TODO: there is definitely a cleaner way to format the cache

        # popping 'cache' flag because storing it messes with how search() works
        if 'cache' in kwargs:
            kwargs.pop('cache')

        with open(self.path, 'a') as f:
            d = {'args' : args,
                'kwargs' : kwargs,
                'data' : data}

            f.write(json.dumps(d) + '\n')

def cacheable(func):
    def wrapper(*args, **kwargs):
        if 'cache' in kwargs:
            cache = kwargs['cache']

        else:
            cache = False

        c = Cache(func.__name__)
        cache_search = c.search(args, kwargs)

        if cache and cache_search:
            return cache_search

        else:
            d = func(*args, **kwargs)
            if not cache_search:
                c.write(d, args, kwargs)

            return d

    return wrapper
