import traffic
import time
import json

# gets traffic data for systems within sphere radius of given system, dumps to json file
#tr = traffic.traffic_radius(system_name = 'Alcor', radius = 10, min_pop = 20000, cache = True)
#print(tr)

def _add_to(file, data):
    with open(file, 'a') as f:
        f.write(data + '\n')

def main():
    ts = traffic.TrafficSphere('Warkawa', 20)
    while True:
        # update sphere
        ts.update()

        # dump to file
        for monitor in ts.monitors.values():
            _add_to('data.txt', json.dumps(monitor.traffic))

        time.sleep(20)

        
