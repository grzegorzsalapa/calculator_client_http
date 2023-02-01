import requests


class CalculationService:

    def __init__(self, server_address: str):
        self.server_address = server_address
        self.PORT = 8080

    def calculate(self, expression):

        payload_out = {'expression': expression}
        url = f'http://{self.server_address}:{self.PORT}/calculations'
        r = requests.post(url, json=payload_out)
        payload_in = r.json()
        if r.status_code != 201:
            return _get_error_message_from_payload(payload_in)

        path = _get_path_from_payload(payload_in)

        url = f'http://{self.server_address}:{self.PORT}' + path
        r = requests.get(url)
        payload_in = r.json()
        if r.status_code != 302:
            return _get_error_message_from_payload(payload_in)

        return _get_result_from_payload(payload_in)

    def get_calculation_by_id(self, calc_id):

        url = f'http://{self.server_address}:{self.PORT}/calculations/{calc_id}'
        r = requests.get(url)
        payload = r.json()
        if r.status_code != 302:
            return _get_error_message_from_payload(payload)

        return _get_calculations_from_payload(payload)

    def get_all_calculations(self):

        url = f'http://{self.server_address}:{self.PORT}/calculations'
        r = requests.get(url)
        print(r.content)
        payload = r.json()
        if r.status_code != 302:
            return _get_error_message_from_payload(payload)

        return _get_calculations_from_payload(payload)


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


def _get_error_message_from_payload(payload):

    try:
        return [payload['detail']]

    except Exception as e:
        raise NameError('Returned error message contains no details.')