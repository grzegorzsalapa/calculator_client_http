from calculator_client import Calculator, CalculationError



def main():
    server_address = _ask_for_server_address()
    calculator = Calculator(server_address)
    try:
        while True:
            expression = _ask_for_expression()

            try:
                result = calculator.calculate(expression)

            except CalculationError as e:
                print(str(e), "\n")

            else:
                print(result, "\n")

    except KeyboardInterrupt:
        calculator.close()
        print("\rBye")


def _ask_for_server_address():
    server_address = input("\nProvide calculation server address:\n")
    print('')
    return server_address


def _ask_for_expression():
    expression = input("Provide simple math expression and press enter, "
                       "only integers allowed:\n")
    return expression


if __name__ == "__main__":
    main()
