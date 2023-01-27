from unittest.mock import MagicMock, patch
from calculator_client.calculate import Calculator, CalculationError
import pytest


def test_that_received_result_on_socket_is_passed_properly_as_a_result_to_calculate():

    def _set_up_mocked_calculator_socket(recv_value=None):
        socket_instance = MagicMock(name="SocketInstance")
        socket_instance.connect = MagicMock()
        socket_instance.recv = MagicMock(return_value=recv_value)

        socket_mock = MagicMock()
        socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_instance)

        return socket_mock

    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with patch('calculator_client.TCP_client.socket', new=socket_mock):
        rc = Calculator('127.0.0.1')
        assert rc.calculate('2+2*2') == '6'


def test_that_correct_binary_representation_of_expression_is_sent_on_socket():

    def _set_up_mocked_calculator_socket(recv_value=None):
        socket_instance = MagicMock(name="SocketInstance")
        socket_instance.connect = MagicMock()
        socket_instance.recv = MagicMock(return_value=recv_value)

        socket_mock = MagicMock()
        socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_instance)

        return socket_mock

    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with patch('calculator_client.TCP_client.socket', new=socket_mock):
        rc = Calculator('127.0.0.1')
        rc.calculate('(2+2)*5/7-3+sde')
        socket_mock.socket().sendall.assert_called_once_with(b'(2+2)*5/7-3+sde')


def test_that_server_address_is_passed_to_socket():

    def _set_up_mocked_calculator_socket(recv_value=None):
        socket_instance = MagicMock(name="SocketInstance")
        socket_instance.connect = MagicMock()
        socket_instance.recv = MagicMock(return_value=recv_value)

        socket_mock = MagicMock()
        socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_instance)

        return socket_mock

    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with patch('calculator_client.TCP_client.socket', new=socket_mock):
        rc = Calculator('127.0.0.1')
        rc.calculate('(2+2)*5/7-3+sde')
        socket_mock.socket().connect.assert_called_once_with(('127.0.0.1', 9010))


def test_that_returned_error_message_is_converted_to_exception():

    def _set_up_mocked_calculator_socket(recv_value=None):
        socket_instance = MagicMock(name="SocketInstance")
        socket_instance.connect = MagicMock()
        socket_instance.recv = MagicMock(return_value=recv_value)

        socket_mock = MagicMock()
        socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_instance)

        return socket_mock

    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'Example error message.')

    with pytest.raises(CalculationError, match=r"Example error message."):
        with patch('calculator_client.TCP_client.socket', new=socket_mock):
            rc = Calculator('127.0.0.1')
            rc.calculate('(2+2)*5/7-3+sde')


def test_timeout_when_no_connection():

    def _set_up_mocked_calculator_socket(recv_value=None):
        socket_instance = MagicMock(name="SocketInstance")
        socket_instance.connect = MagicMock(side_effect=ConnectionRefusedError)
        socket_instance.recv = MagicMock(return_value=recv_value)

        socket_mock = MagicMock()
        socket_mock.socket = MagicMock(name="SocketModule", return_value=socket_instance)

        return socket_mock

    socket_mock = _set_up_mocked_calculator_socket(recv_value=b'6')

    with pytest.raises(CalculationError, match=r"Several attempts to access the remote calculator failed.\n"
                                               "Try again..."):
        with patch('calculator_client.TCP_client.socket', new=socket_mock):
            rc = Calculator('127.0.0.1')
            rc.remote_service.sleep_time = 0
            rc.calculate('any')
