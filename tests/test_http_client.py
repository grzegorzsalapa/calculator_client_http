import pytest
from calculator_client.http_client import CalculationService
import responses


@responses.activate
def test_returns_correct_expression_result():

    def _test_prep():
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

    _test_prep()
    calculator = CalculationService('127.0.0.1')

    assert calculator.calculate('2 + 2') == "4"


@responses.activate
def test_returns_calculation_results_bi_id():

    resp1 = responses.Response(
        method="GET",
        url="http://127.0.0.1:8080/calculations/5",
        json=[{"id": "1", "expression": "2 + 2", "result": "4"}]
    )

    responses.add(resp1)
    calculator = CalculationService('127.0.0.1')

    assert calculator.get_calculation_by_id('5') == ["id 1: 2 + 2 = 4"]


@responses.activate
def test_returns_all_calculation_results():

    resp1 = responses.Response(
        method="GET",
        url="http://127.0.0.1:8080/calculations",
        json=[{"id": "1", "expression": "2 + 2", "result": "4"},
              {"id": "2", "expression": "3 + 3", "result": "6"},
              {"id": "3", "expression": "4 + 4", "result": "8"}]
    )

    responses.add(resp1)
    calculator = CalculationService('127.0.0.1')

    assert calculator.get_all_calculations() == ['id 1: 2 + 2 = 4',
                                                 'id 2: 3 + 3 = 6',
                                                 'id 3: 4 + 4 = 8']
