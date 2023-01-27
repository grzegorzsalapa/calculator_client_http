import requests
import re
import json


class RemoteCalculationError(Exception):
    pass


class RemoteService:

    def __init__(self, server_address: str):
        self.server_address = server_address
        self.PORT = 8080

    def calculate(self, expression):
        data_out = {'expression': expression}

        return self.get_response(data_out)

    def get_response(self, data):
        url = f'http://{self.server_address}:{self.PORT}/calculations'
        r = requests.post(url, json=data)
        json_in = r.json()

        path = _get_path_from_json(json_in)

        url = f'http://{self.server_address}:{self.PORT}' + path
        r = requests.get(url)
        json_in = r.json()

        result = _get_result_from_json(json_in)

        return result

def _get_path_from_json(payload):

    return payload['url']

def _get_result_from_json(payload):

    return payload[0]['result']