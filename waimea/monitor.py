import json
import requests
import random
from time import sleep

from waimea.config import API_HOST, API_PORT

# TODO: add function that simulates gradual, more realistic tides
# def randomize_wave_height(initial_height: int, previous_height: int, volatility: float, bottom: int, top: int) -> list:
#     while True:
#         wave_height = previous_height + initial_height * random.gauss(0, 1) * volatility # markov process that simulates random time series data
#         if wave_height >= bottom and wave_height <= top: # check to keep synthetic MR values within a realistic range
#             return int(round(wave_height))

def main():
    # TODO:
    #  10x per second:
    #    1) Generate a random wave height
    #    2) Send wave height to the data/log to the http://API_HOST:API_PORT/log endpoint

    while True:
        random_height = random.randint(0, 85) # 85 foot record at Waimea Bay
        sleep(0.09)

        serialized_data = json.dumps(random_height)
        requests.post('http://api:8080/log', data=serialized_data)
