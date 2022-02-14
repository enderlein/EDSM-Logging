import requests
import json

def cache_check(sys_name = '', sys_id = '', file = './cache/traffic'): 
    # check cache for existing entry by name or id
    # prioritizes lookup by system id (if id is provided)
    with open(file, 'r') as f:
        for line in f: #assuming every line holds a traffic data obj, which it should
            obj = json.loads(line)
            if sys_id:
                if sys_id == obj['id']:
                    return obj

            elif sys_name:
                if sys_name == obj['name']:
                    return obj

            else:
                return False

#def cache_write(data, file = 'traffic_cache'):
#    with open(file, 'a')

def traffic(system_name, file = './cache/traffic'):
    # check if system traffic data is in cache already
    c = cache_check(sys_name = system_name)

    if c:
        print(f'Got {system_name} from cache')
        return c

    # if not in cache get from api and add to cache
    else:
        params = {'systemName' : system_name}
        r = requests.get('https://www.edsm.net/api-system-v1/traffic', params = params)

        print(f'Got {system_name} from API')

        d = json.loads(r.text)

        # make standalone cache_write function
        with open(file, 'a') as f:
            f.write(f'{json.dumps(d)}\n')
            print(f'Wrote {system_name} to cache')
        return d



print(traffic('Warkawa'))
print()
print(traffic('Sol'))
print()
print(traffic('Itzamnets'))

