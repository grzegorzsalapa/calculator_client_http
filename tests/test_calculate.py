from unittest.mock import MagicMock, patch
from calculator_client.calculate import Calculator
import pytest
import responses


@responses.activate
def test_returns_correct_expression_result():
    resp1 = responses.Response(
        method="POST",
        url="http://127.0.0.1:8080/calculations",
        json={"url": "/calculations/1"}
    )

    resp2 = responses.Response(
        method="GET",
        url="http://127.0.0.1:8080/calculations/1",
        json=[{"id": "1", "expression": "2 + 2", "result": "4"}]
    )

    responses.add(resp1)
    responses.add(resp2)

    calculator = Calculator('127.0.0.1')
    calculator.calculate('2 + 2')

    assert calculator.calculate('2 + 2') == "4"
