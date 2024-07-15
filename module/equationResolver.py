from errors.errors import *
from enums.enums import *
from math import sin, cos, tan, pi, factorial


def compute_basic_equation(initial_string):
    """calls other functions:\n
    computing trigonometric functions, factorial, exponentiation, multiplication/division, addition/subtraction"""
    return conduct_addition(
        conduct_multiplication(conduct_exponentiation(compute_factorial(compute_trigon(initial_string)))))


def find_parenthesis(str):
    """find_parenthesis(str) -> left_parenthesis_index, right_parenthesis_index\n
    returns tuple with two lists where
    left_parenthesis_index stores indexes of '(' and right_parenthesis_index stores indexes of ')'\n
    throws exception when numer of '(' and ')' does not match"""
    counter = 0
    left_parenthesis_index = []
    right_parenthesis_index = []
    for i, ch in enumerate(str):
        if ch == '(':
            counter += 1
            left_parenthesis_index.append(i)
        elif ch == ')':
            counter -= 1
            right_parenthesis_index.append(i)
    if counter != 0:
        raise WrongParenthesisError("Wrong nuber of parenthesis")
    return left_parenthesis_index, right_parenthesis_index


def get_min_distance_index_list(tuple):
    """get_min_distance_index_list(tuple) -> list\n
    tuple has two lists which contains indexes of '(' and indexes of ')'\n
    returns two-element list with indexes od the closest parenthesis"""
    minimum = max(tuple[1]) - min(tuple[0])
    min_distance_index_lst = [0, 0]
    # search indexes of left and right parenthesis closest to each other
    for j in tuple[0]:
        for k in tuple[1]:
            # k > j means that right parenthesis is on the left of left parenthesis
            if minimum >= (k - j) > 0 and k > j:
                min_distance_index_lst[0] = j
                min_distance_index_lst[1] = k
                minimum = k - j
    # add 1 for right parenthesis to be included
    min_distance_index_lst[1] += 1
    return min_distance_index_lst


def cut_and_compute(initial_string, index_lst):
    """Takes string, makes operation on part of string between two indexes (included) given in index_lst
    and then returns whole string"""
    x, z = index_lst
    mid_to_compute = (initial_string[x:z])
    left_string = initial_string[0:x]
    right_string = initial_string[z:len(initial_string)]
    return left_string + compute_par(mid_to_compute) + right_string


def compute_par(string):
    """Excludes parenthesis and returns computed value.
    Computed value for raw float is returned immediately, for other equations there is called function computing it."""
    if string[0] == '(' and [len(string) - 1] == ')':
        equation = string[2:len(string) - 2]
    else:
        equation = string[1:len(string) - 1]
    try:
        # if parenthesis contains float e.g. string=(4.2) then return this float value
        float(equation)
        return equation
    except ValueError:
        return compute_basic_equation(equation)


def compute_equation(initial_string):
    """this function is called first while computing equation"""
    if not any(ch.isdigit() for ch in initial_string):
        raise NoNumberInInput("input han no numbers")
    initial_string = del_spaces(initial_string)
    while '(' in initial_string or ')' in initial_string:
        parenthesis_indexes_all = find_parenthesis(initial_string)
        closest_parenthesis_indexes = get_min_distance_index_list(parenthesis_indexes_all)
        initial_string = cut_and_compute(initial_string, closest_parenthesis_indexes)
    if '(' not in initial_string or ')' not in initial_string:
        return compute_basic_equation(initial_string)
    return initial_string


def compute_trigon(initial_string):
    """Transforms string in a way that trigonometric functions sin, cos, tan, ctg in string are calculated"""
    trigon_search = ['sin', 'cos', 'tan', 'ctg']
    trigon_acceptable = ['+', '-', '.']
    for trigon_function in trigon_search:
        while trigon_function in initial_string:
            index = initial_string.find(trigon_function)
            right_side_string_index = index + 3  # +3 means after sin or cos etc.
            if right_side_string_index >= len(initial_string):
                raise LackOfOperandAtTheEndOfEquation("Lack of " + trigon_function + " function argument")
            ch = initial_string[right_side_string_index]
            maybe_number = ''
            while ch in trigon_acceptable or ch.isdigit():
                maybe_number += ch
                right_side_string_index += 1
                if right_side_string_index < len(initial_string):
                    ch = initial_string[right_side_string_index]
                    if (ch == '+' or ch == '-') and initial_string[right_side_string_index - 1].isdigit():
                        break
                else:
                    ch = 'anything'  # it is NOT an exception
            try:
                last_character = maybe_number[len(maybe_number) - 1]
            except IndexError:
                raise LackOfTrigonometricFunctionArgument("lack of " + trigon_function + " argument")
            if last_character == '+' or last_character == '-':
                maybe_number = maybe_number[:-1]  # without last + or -
                right_side_string_index -= 1
            left_string = initial_string[0:index]   # something before trigonometric function
            right_string = initial_string[right_side_string_index:len(initial_string)]  # after trigonometric function
            number = convert_to_number(maybe_number)
            match trigon_function:
                case 'sin':
                    number = round(sin(radians(number)), 14)
                case 'cos':
                    number = round(cos(radians(number)), 14)
                case 'tan':
                    if (number + 90) % 180 == 0:
                        raise OutOfFunctionDomain("Tangent of " + str(number) + "° cannot be calculated")
                    number = round(tan(radians(number)), 14)
                case 'ctg':
                    if number % 180 == 0:
                        raise OutOfFunctionDomain("Cotangent of " + str(number) + "° cannot be calculated")
                    number = round(1 / tan(radians(number)), 14)
            result = str(number)
            initial_string = left_string + result + right_string
    return del_letters(initial_string)  # after computing trigonometric functions other letters are not needed


def convert_to_number(maybe_number):
    """Changes string into float, if not convertible raises exception"""
    try:
        number = float(maybe_number)
        return number
    except ValueError:
        raise NotConvertableToFloatError(maybe_number + " is not a number.")


def radians(number):
    return number * pi / 180


def compute_factorial(initial_string):
    """Transforms string in a way that factorials in string are calculated\n
    Number on the left side of exclamation mark must string convertable to integer number"""
    while '!' in initial_string:
        index = initial_string.find('!')
        right_side_string_index = index + 1
        left_side_string_index = index - 1
        if left_side_string_index < 0:
            raise LackOfOperandAtTheBeginningOfEquation("Lack of factorial argument")
        ch = initial_string[left_side_string_index]
        maybe_integer = ''
        while ch.isdigit() or ch == '.':
            maybe_integer += ch
            left_side_string_index -= 1
            if left_side_string_index >= 0: # make sure that index in not less than 0.
                ch = initial_string[left_side_string_index]
            else:
                ch = 'anything'
        maybe_integer = maybe_integer[::-1]  # reverse
        left_string = initial_string[0:left_side_string_index + 1]
        right_string = initial_string[right_side_string_index:len(initial_string)]
        number = convert_to_integer(maybe_integer)
        result = str(factorial(number))
        initial_string = left_string + result + right_string
    return initial_string


def convert_to_integer(maybe_integer):
    try:
        number = int(maybe_integer)
        return number
    except ValueError:
        raise NotConvertableToIntegerError(maybe_integer + " is not an integer.")


def conduct_exponentiation(initial_string):
    """Transform string in a way that exponentiation is calculated
    by calling function named compute_two_operands_operations"""
    return compute_two_operands_operations(initial_string, ['^'])


def conduct_multiplication(initial_string):
    """Transform string in a way that multiplication and division is calculated
    by calling function named compute_two_operands_operations"""
    return compute_two_operands_operations(initial_string, ['*', '/'])


def conduct_addition(initial_string):
    """Transform string in a way that addition and subtraction is calculated
    by calling function named compute_two_operands_operations"""
    return compute_two_operands_operations(initial_string, ['+', '-'])


def compute_two_operands_operations(initial_string, operations_list):
    """Transform string in a way that operations given as 2nd argument are calculated"""
    operators = []
    initial_string = remove_adjacent_plus_and_minus(initial_string)
    if initial_string[0] == '-' and not ('^' in operations_list):
        initial_string = '0' + initial_string

    for character in initial_string:
        if character in operations_list:
            operators.append(character)

    for i, operator in enumerate(operators):
        if initial_string[0] == '-' and operator == '-':
            index = find_second_occurrence(initial_string, operator)
        else:
            index = initial_string.find(operator)
        right_side_string_index = index + 1
        left_side_string_index = index - 1
        if left_side_string_index < 0:
            if not (operator == '-' or operator == '+'):  # + or - can be at the beginning
                raise LackOfOperandAtTheBeginningOfEquation(
                    "While conducting operation of" + operator_to_text(operator))
        elif right_side_string_index >= len(initial_string):
            raise LackOfOperandAtTheEndOfEquation("While conducting operation of" + operator_to_text(operator))

        maybe_float_left, left_side_string_index \
            = get_right_or_left_operand(initial_string, left_side_string_index, Operand.LEFT)
        maybe_float_right, right_side_string_index \
            = get_right_or_left_operand(initial_string, right_side_string_index, Operand.RIGHT)
        if operator == '^' and left_side_string_index != 0:
            left_side_string_index += 1
        left_string = initial_string[0:left_side_string_index]
        right_string = initial_string[right_side_string_index:len(initial_string)]
        number_right = convert_to_number(maybe_float_right)
        number_left = convert_to_number(maybe_float_left)

        result = calculate_two_operands_operation(number_left, number_right, operator)
        initial_string = left_string + str(result) + right_string
    return initial_string


def find_second_occurrence(initial_string, operator):
    """returns index of second occurrence of given operator"""
    index = initial_string.find(operator)
    index += 1
    initial_string = initial_string[index:len(initial_string)]
    return index + initial_string.find(operator)


def operator_to_text(operator):
    match operator:
        case '*':
            return " multiplication"
        case '/':
            return " division"
        case '^':
            return " exponentiation"
        case '+':
            return " addition"
        case '-':
            return " subtraction"


def get_right_or_left_operand(initial_string, index, operand_type):
    ch = initial_string[index]
    maybe_number = ''
    ch_acceptable = ['+', '-', '.']
    other_operations = ['*', '/', '^']
    while ch.isdigit() or ch in ch_acceptable:

        maybe_number += ch

        if operand_type == Operand.LEFT:
            index -= 1
            if index >= 0:
                if (ch == '+' or ch == '-') and initial_string[index + 2].isdigit():
                    index += 1
                    break
                ch = initial_string[index]
                if ch in other_operations:
                    index += 1
            else:
                index += 1
                ch = 'anything'
        elif operand_type == Operand.RIGHT:
            index += 1
            if index < len(initial_string):
                ch = initial_string[index]
                if (ch == '+' or ch == '-') and initial_string[index - 1].isdigit():
                    break
            else:
                ch = 'anything'
    if operand_type == Operand.LEFT:

        maybe_number = maybe_number[::-1]  #reverse
        first_element = maybe_number[0]
        if first_element == '+':
            maybe_number = maybe_number[1:]  #delete first
            index += 1  #include sign "+"
        return maybe_number, index
    else:
        return maybe_number, index


def calculate_two_operands_operation(numer_left, number_right, operator):
    match operator:
        case '*':
            return round(numer_left * number_right, 14)
        case '/':
            if number_right == 0:
                raise DivisionByZero(str(numer_left) + "/" + str(number_right) + " is not allowed")
            return round(numer_left / number_right, 14)
        case '^':
            return round(numer_left ** number_right, 14)
        case '+':
            return round(numer_left + number_right, 14)
        case '-':
            return round(numer_left - number_right, 14)


def remove_adjacent_plus_and_minus(initial_string):
    operators = ['+', '-']
    indexes_to_remove = set()
    initial_string = list(initial_string)
    for i in range(1, len(initial_string)):
        previous = initial_string[i - 1]
        current = initial_string[i]
        if current in operators and previous in operators:
            if current == previous:
                indexes_to_remove.add(i)
            elif current == '+':
                indexes_to_remove.add(i)
            else:
                indexes_to_remove.add(i - 1)

    for i, ch in enumerate(initial_string):
        if i in indexes_to_remove:
            initial_string[i] = ' '

    return del_spaces(initial_string)


def del_spaces(initial_string):
    """returns string without spaces"""
    return ''.join([x for x in initial_string if x != ' '])


def del_letters(initial_string):
    """returns string without letters"""
    return ''.join([x for x in initial_string if not x.isalpha()])
