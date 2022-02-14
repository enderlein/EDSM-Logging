import requests
import json
import caching

def traffic(system_name, file = './cache/traffic'):
    # check if system traffic data is in cache already
    c = caching.Cache('traffic')

    url = "https://www.edsm.net/api-system-v1/traffic"
    params = {'systemName' : system_name}

    cache_search = c.search(url, params)
    if cache_search:
        print(f'Got {system_name} from cache')
        return cache_search

    # if not in cache get from api and add to cache
    else:
        r = requests.get(url, params = params)

        print(f'Got {system_name} from API')

        d = json.loads(r.text)

        # add to cache
        c.write(url, params, d)
        return d



print(traffic('Warkawa'))
print()
print(traffic('Sol'))
print()
print(traffic('Itzamnets'))

