import traffic
import time
import json

# Turns out traffic API only updates once per commander per ship.
# Can't track players in real time, but old traffic data might show popular routes??
# Then again, its easy to opt out of being tracked, and anyone who would want to would, so
# I'd really only be tracking players who wanted to be tracked
# What to doooooooooooo

def append_file(file, data):
    with open(file, 'a') as f:
        f.write(data + '\n')

def log_traffic(system_name, sleep):
    # create TrafficMonitor object for given star system
    tm = traffic.TrafficMonitor(system_name)

    while True:
        # update monitor
        tm.update()

        # serialize traffic data (dict) into (str)
        s = json.dumps(tm.traffic)

        # log in file
        filename = f"traffic_{tm.traffic['system_name']}.txt"
        append_file(filename, s)

        # sleep
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Sleeping: {sleep} seconds... (since {current_time})")
        time.sleep(sleep)

def detect_traffic_update(system_name, sleep):
    # create TrafficMonitor object for given star system
    tm = traffic.TrafficMonitor(system_name)

    while True:
        # update monitor
        tm.update()

        # check diff property
        if tm.diff != None:
            if tm.diff['traffic']['day'] > 0:
                # instead of printing, you could return a value to a watchdog somewhere
                print(f"Update detected: {tm.diff['traffic']['day']} new ships\n" + 
                              f"Location: {tm.diff['system_name']}\n" + 
                              f"since last update (approx. {tm.diff['timestamp']} seconds ago)")
                print(f"Ship breakdown: {tm.diff['breakdown']}")

        #sleep for 30 seconds
        print("Sleeping...")
        time.sleep(sleep)
