import traffic
import edsm

# gets traffic data for systems within sphere radius of given system, dumps to json file
tr = traffic.traffic_radius(system_name = 'Alcor', radius = 10, min_pop = 20000, cache = True)
print(tr)