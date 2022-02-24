import sqlite3

import sqlite3_wrapper
import traffic

tr = traffic.traffic_radius(system_name = 'Alcor', radius = 20, min_pop = 20000, dumps = True, use_cache = False)