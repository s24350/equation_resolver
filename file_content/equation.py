class Equation:
    def __init__(self, equation_id, equation, result):
        self.equation_id = equation_id
        self.equation_string = equation
        self.result = result

    def __str__(self):
        return f"{self.equation_id}\t{self.equation_string}\t{self.result}"

    def to_string(self):
        return f"{self.equation_id}:\t{self.equation_string}=\t{self.result}"


def get_max_id(equation_list):
    max_id = 0
    for e in equation_list:
        max_id = int(e.equation_id)
    return str(max_id+1)


def print_eq_list(equation_list):
    for e in equation_list:
        print(e.to_string())

