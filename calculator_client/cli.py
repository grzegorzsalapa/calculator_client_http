from calculator_client import CalculationService


def main():
    server_address = _ask_for_server_address()
    calculator = CalculationService(server_address)
    try:
        while True:

            _ask_for_option_choice(calculator)

    except KeyboardInterrupt:
        print("\rBye")


def _ask_for_server_address():
    server_address = input("\nProvide calculation server address:\n")
    print('')
    return server_address

def _ask_for_option_choice(calculator):
    selection = input("What would you like to do:\n"
                      "- calculate expression (c)\n"
                      "- show all calculations you made (a)\n"
                      "- show calculation providing its id (i)\n")

    if selection == "c":
        expression = _ask_for_expression()
        result = calculator.calculate(expression)
        print(result, "\n")

    elif selection == "a":
        calculations = calculator.get_all_calculations()
        _print_calculations(calculations)

    elif selection == "i":
        calc_id = _ask_for_calculation_id()
        calculations = calculator.get_calculation_by_id(calc_id)
        _print_calculations(calculations)

    else:
        _ask_for_option_choice()


def _ask_for_calculation_id():

    return input("\nProvide calculation id:\n")


def _ask_for_expression():

    return input("\nProvide simple math expression and press enter, only integers allowed:\n")


def _print_calculations(calculations):

    print('')
    for calc in calculations:
        print(calc)
    print('')

if __name__ == "__main__":
    main()
