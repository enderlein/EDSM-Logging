import json
import time
import logging

from logging import INFO, DEBUG

import edsm.models as models
import edsm.config as config


"""
For storing timstamped system data.

Made for collecting live system data from edsm.net to help spot trends in market and traffic data.
"""

# TODO: Finish annotating

# TODO: ABCs lol

logging.basicConfig(level=INFO)

class Logger():
    def __init__(self, keys:dict[str, list[str]]):
        self.keys = keys

        self.systems = models.Systems()

        # to be overwritten by children (TODO: ABCs lol)
        self.filename = f'{self}.json'


    def update_by_keys(self):
        """
        Run updates depending on which keys are provided. 
        """
        if 'traffic' in self.keys:
            logging.info("Updating traffic")
            self.systems.update_traffic()

        if 'stations' in self.keys:
            logging.info("Updating stations")
            self.systems.update_stations()

            if 'market' in self.keys['stations']:
                logging.info("Updating station markets")
                self.systems.update_stations_markets()

    def generate_payload(self) -> list[dict]:
        """
        Package and timestamp requested data
        """
        logging.info("Generating payload")

        timestamp = int(time.time())
        data = self.systems.get_keys(self.keys)

        return [{'timestamp' : timestamp, 'data' : data}]

    #TODO: Change something here to specify that this func only appends arrays (maybe rename to append_json_array())
    def append_json(self, file:str, data:list[dict]):
        """
        Appends json data to .json file.
        Assumes that file is either empty or has top-level JSON array.
        """

        # default old_data to empty list if given file doesn't exist or has invalid json (really only want to check for empty files, 
        # should stop/throw warning if there is data but its not valid json. TODO: narrow second exception)
        logging.info(f"Appending payload to file: \'{self.filename}\'")
        try:
            file_read = open(file, 'r')
            old_data = json.loads(file_read.read())
            file_read.close()
                
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # TODO: log exception (as warning)
            old_data = []

        merged_data = json.dumps(old_data + data, indent=config.JSON_INDENT)

        file_write = open(file, 'w')
        file_write.write(merged_data)

        file_write.close()

    def log(self):
        logging.info("Beginning log routine")

        self.update_by_keys()

        payload = self.generate_payload()
        self.append_json(self.filename, payload)
    
    def sleep(self, delay):
        sleep_start = time.strftime("%H:%M:%S", time.localtime())
        logging.info(f"{self} SLEEPING for {delay} seconds (since {sleep_start})")

        time.sleep(delay)

    def run(self, sleep:int=config.DEFAULT_SLEEP):
        """Run self.log() and sleep for `sleep` seconds on an infinite loop"""
        while True:
            self.log()
            self.sleep(sleep)
