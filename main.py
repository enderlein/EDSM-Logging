import traffic
import time
import json

def append_file(file, data):
    with open(file, 'a') as f:
        f.write(data + '\n')

def log_traffic(system_name):
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

        # sleep for 5 minutes
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Sleeping: 5 minutes... (since {current_time})")
        time.sleep(300)

def detect_traffic_update(system_name):
    # create TrafficMonitor object for given star system
    tm = traffic.TrafficMonitor(system_name)

    while True:
        # update monitor
        tm.update()

        # check diff property
        if tm.diff != None:
            if tm.diff['traffic']['day'] > 0:
                print(f"Update detected: {tm.diff['traffic']['day']} new ships\n" + 
                              f"Location: {tm.diff['name']}\n" + 
                              f"since last update (approx. {tm.diff['timestamp']} seconds ago)")
                print(f"Ship breakdown: {tm.diff['breakdown']}")

        #sleep for 30 seconds
        print("Sleeping...")
        time.sleep(30)
