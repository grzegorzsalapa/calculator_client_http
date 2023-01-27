from .TCP_client import RemoteService, RemoteCalculationError


class CalculationError(Exception):

    def __init__(self, message: str):
        self.message = message


class Calculator:

    def __init__(self, server_address):
        self.server_address = server_address
        self.remote_service = RemoteService(self.server_address)

    def calculate(self, expression: str):
        try:
            return self.remote_service.calculate(expression)

        except RemoteCalculationError as e:
            raise CalculationError(str(e))

        except TimeoutError as e:
            raise CalculationError(str(e))

    def close(self):
        self.remote_service.disconnect()
