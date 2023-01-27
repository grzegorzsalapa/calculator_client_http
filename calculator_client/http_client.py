import requests


class CalculationService:

    def __init__(self, server_address: str):
        self.server_address = server_address
        self.PORT = 8080

    def calculate(self, expression):

        payload = {'expression': expression}
        url = f'http://{self.server_address}:{self.PORT}/calculations'
        r = requests.post(url, json=payload)
        json_in = r.json()

        path = _get_path_from_payload(json_in)

        url = f'http://{self.server_address}:{self.PORT}' + path
        r = requests.get(url)
        json_in = r.json()

        result = _get_result_from_payload(json_in)

        return result

    def get_calculation_by_id(self, calc_id):

        url = f'http://{self.server_address}:{self.PORT}/calculations/{calc_id}'
        r = requests.get(url)
        payload = r.json()

        calculation = _get_calculations_from_payload(payload)

        return calculation

    def get_all_calculations(self):

        url = f'http://{self.server_address}:{self.PORT}/calculations'
        r = requests.get(url)
        payload = r.json()

        calculations = _get_calculations_from_payload(payload)

        return calculations


def _get_calculations_from_payload(calc_list):

    calculations = []
    for calculation in calc_list:
        calc_id = calculation['id']
        expression = calculation['expression']
        result = calculation['result']
        calculations.append(f"id {calc_id}: {expression} = {result}")

    return calculations


def _get_path_from_payload(payload):

    return payload['url']


def _get_result_from_payload(calc_list):

    return calc_list[0]['result']