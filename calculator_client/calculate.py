from .http_client import RemoteService, RemoteCalculationError


class Calculator:

    def __init__(self, server_address):
        self.server_address = server_address
        self.remote_service = RemoteService(self.server_address)

    def calculate(self, expression: str):
        try:
            return self.remote_service.calculate(expression)

        except TimeoutError as e:
            raise CalculationError(str(e))

    def close(self):
        self.remote_service.disconnect()
