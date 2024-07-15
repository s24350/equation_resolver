class WrongParenthesisError(Exception):
    pass


class NotConvertableToFloatError(Exception):
    pass


class NotConvertableToIntegerError(Exception):
    pass


class OutOfFunctionDomain(Exception):
    pass


class LackOfOperandAtTheEndOfEquation(Exception):
    pass


class LackOfOperandAtTheBeginningOfEquation(Exception):
    pass


class LackOfTrigonometricFunctionArgument(Exception):
    pass


class DivisionByZero(Exception):
    pass


class NoNumberInInput(Exception):
    pass
