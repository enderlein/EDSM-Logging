import traffic
import edsm
import asyncio

# gets traffic data for systems within sphere radius of given system, dumps to json file
#tr = traffic.traffic_radius(system_name = 'Alcor', radius = 10, min_pop = 20000, cache = True)
#print(tr)

ts = traffic.TrafficSphere('Warkawa', 20)

async def main():
    print([t.traffic for t in ts.monitors.values()])
    await ts.update()
    print([t.traffic for t in ts.monitors.values()])

    # input() is here to prevent bug in aiohttp module which raises 'RuntimeError: Event loop is closed' on exit
    # Not sure, but I think this happens because aiohttp.ClientSession() (accessed in edsm.py) doesn't close
    # itself fast enough (doesn't close before garbage collection happens)
    input()

asyncio.run(main())
