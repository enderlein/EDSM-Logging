import sqlite3

import sqlite3_wrapper
import traffic

# gets traffic data for systems within sphere radius of given system, dumps to json file
tr = traffic.traffic_radius(system_name = 'Alcor', radius = 20, min_pop = 20000, dumps = True, use_cache = False)