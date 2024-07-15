from file_content.equation import Equation


def read_file(filename):
    file = open(filename, "r")
    read_content = file.read()
    equations_string_list = read_content.split('\n')
    return equations_string_list


def convert_to_objects(equations_string_list):
    eq_list = []
    try:
        for e in equations_string_list:
            e_id, eq_str, res = e.split('\t')
            eq = Equation(e_id, eq_str, res)
            eq_list.append(eq)
    except ValueError:
        return eq_list
    return eq_list


def save_into_file(eq):
    with open("equations.txt", "a") as file:
        file.write(str(eq)+"\n")


def del_last_character(string):
    return string[0:len(string)-1]
