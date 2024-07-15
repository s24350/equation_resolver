from file_content.file import *
from file_content.equation import *
from module.equationResolver import *

print("Calculator\n"
      "basic operations:\t"
      "addition: '+'\tsubtraction: '-'\tmultiplication: '*'\tdivision: '/'\texponentiation: '^'\n"
      "trigonometry:\t"
      "sinus: 'sin' \tcosine: 'cos'\ttangent: 'tan'\tcotangent: 'ctg'\n"
      "one operand operation:\tfactorial: '!\n"
      "using round brackets legal\n"
      "history of operations: 'history'\n"
      "exit calculator: 'quit'\n")
input_string = input("Enter input: ")
equation_list = convert_to_objects(read_file("equations.txt"))

while input_string != 'quit':
    if input_string == 'history':
        print_eq_list(equation_list)
    else:
        equation_id = get_max_id(equation_list)
        equation_string = input_string
        result = ''

        try:
            result = compute_equation(input_string)
        except OutOfFunctionDomain as e:
            print(e)
            result = 'error'
        except DivisionByZero as e:
            print(e)
            result = 'error'
        except NoNumberInInput as e:
            print(e)
            result = 'error'
        except LackOfTrigonometricFunctionArgument as e:
            print(e)
            result = 'error'
        except LackOfOperandAtTheBeginningOfEquation as e:
            print(e)
            result = 'error'
        except LackOfOperandAtTheEndOfEquation as e:
            print(e)
            result = 'error'
        except WrongParenthesisError as e:
            print(e)
            result = 'error'
        except NotConvertableToFloatError as e:
            print(e)
            result = 'error'
        except NotConvertableToIntegerError as e:
            print(e)
            result = 'error'
        equation = Equation(equation_id, equation_string, result)
        equation_list.append(equation)
        save_into_file(equation)
        print("equation: " + equation.to_string())
    input_string = input("Enter input: ")
