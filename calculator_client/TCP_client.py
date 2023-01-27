import socket
import time


class RemoteCalculationError(Exception):
    pass


class RemoteService:

    def __init__(self, server_address: str):
        self.server_address = server_address
        self.PORT = 9010
        self.socket = None
        self.timeout = 20
        self.sleep_time = 5

    def calculate(self, expression: str):
        expr = expression
        while True:
            result = self._get_result(expr)
            if result is not None:
                break
        return result

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def _connect_if_not_yet(self):
        if self.socket is None:
            self._connect()

    def _connect(self):
        count = 0
        limit = 4

        while True:
            try:
                self._connect_on_socket()
                count = 0
                break

            except ConnectionRefusedError:
                count += 1
                time.sleep(self.sleep_time)
                if count > limit:
                    raise TimeoutError("Several attempts to access the remote calculator failed.\n"
                                       "Try again...")

    def _connect_on_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"    Connecting to remote calculator on {self.server_address}")
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.server_address, self.PORT))
            print(f"\r    Successfully connected to remote calculator.")

        except ConnectionRefusedError as e:
            self.disconnect()
            print("   ", str(e), "\n")
            raise

    def _get_result(self, expression):
        self._connect_if_not_yet()
        try:
            expr_b = bytes(expression, 'utf-8')
            self.socket.sendall(expr_b)
            result_b = self.socket.recv(1024)
            while not result_b:
                raise BrokenPipeError
            response = str(result_b)[2:][:-1]
            _check_if_error_returned(response)

            return response

        except (BrokenPipeError, ConnectionResetError):
            print("\n    Connection lost.\n")
            self.disconnect()


def _check_if_error_returned(str_to_check):
    try:
        float(str_to_check)

    except ValueError:
        error_message = str_to_check
        raise RemoteCalculationError(error_message)
