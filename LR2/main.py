from prettytable import PrettyTable
keywords = [
    "int",
    "float",
    "string",
    "if",
    "else",
    "for",
    "while",
    "do",
    "continue",
    "break",
    "print",
    "cout"
]

simple_arith_operators = [
    "+",
    "-",
    "*",
    "/",
    "%"
]

comparison_operators = [
    "==",
    "!=",
    "<=",
    ">=",
    "<",
    ">"
]

all_arith_operators = [
    "+",
    "-",
    "*",
    "/",
    "%",
    "+=",
    "-=",
    "*=",
    "/=",
    "%="
]
delimeters = [
    "(",
    ")",
    ",",
    ";",
    "{",
    "}"
]

f = open("input.txt")
text = f.read()
state = "start"
lex = ""
i = 0

type = ""
line = 1
pos = 0
error_msg = ""

def counter():
    global i
    global pos

    pos += 1
    i += 1


if __name__ == '__main__':
    keyword_table = PrettyTable()
    variable_table = PrettyTable()
    delimeter_table = PrettyTable()
    operator_table = PrettyTable()
    const_table = PrettyTable()
    keyword_table.field_names = ["Keyword", "Description"]
    variable_table.field_names = ["Variable", "Description"]
    delimeter_table.field_names = ["Separator", "Description"]
    operator_table.field_names = ["Operator", "Description"]
    const_table.field_names = ["Constant", "Description"]
    is_float = False
    variables = {}
    while True:
        if state == "start":

            if i == len(text):
                state = "end"
            elif text[i] == ' ' or text[i] == '\n':
                if (text[i] == '\n'):
                    type = ""
                    line += 1
                    pos = 0
                counter()
            elif text[i].isalpha():
                lex = ""
                lex += text[i]
                counter()
                state = "id"
            elif text[i].isdigit():
                is_float = False
                lex = ""
                lex += text[i]
                counter()
                state = "number"
            elif text[i] == "!" or text[i] == "=" or text[i] == "<" or text[i] == ">" or text[i] in simple_arith_operators:
                lex = ""
                lex += text[i]
                counter()
                state = "operator"
            elif text[i] == '"':
                 lex = ""
                 lex += text[i]
                 counter()
                 state = "string"
            else:
                state = "separator"
        elif state == "id":
            if i != len(text) and (text[i].isalpha() or text[i].isdigit() or text[i] == "_"):
                lex += text[i]
                counter()
            else:
                if lex in keywords:
                    keyword_table.add_row([lex, "keyword"])
                    if lex == "int" or lex == "float" or lex == "string":
                        type = lex
                else:
                    if lex not in variables and type == "":
                        error_msg = " Unresolved reference"
                        state = "error"
                        continue
                    if (lex not in variables):
                        variables[lex] = type
                    variable_table.add_row([lex, f"{variables.get(lex)} variable"])
                lex = ""
                state = "start"
        elif state == "number":

            if i != len(text) and text[i].isdigit():
                lex += text[i]
                counter()
            elif i != len(text) and text[i] == ".":
                if (is_float == True):
                    error_msg = "incorrect value"
                    state = "error"
                is_float = True
                lex += text[i]
                counter()
            elif i != len(text) and text[i].isalpha():
                lex += text[i]
                error_msg = "incorrect value"
                state = "error"
            else:
                if is_float:
                    const_table.add_row([lex, "float const"])
                else:
                    const_table.add_row([lex, "int const"])
                lex = ""
                state = "start"
        elif state == "operator":
            if i != len(text) and (text[i] == "!" or text[i] == "=" or text[i] == "<" or text[i] == ">" or text[i] in simple_arith_operators):
                lex += text[i]
                counter()
            else:
                if lex == "=":
                    operator_table.add_row([lex, "assignment operator"])
                elif lex == "<<":
                    operator_table.add_row([lex, "bitwise left shift operator"])
                elif lex in comparison_operators:
                    operator_table.add_row([lex, "comparison operator"])
                elif lex in all_arith_operators:
                    operator_table.add_row([lex, "arithmetical operator"])
                else:
                    error_msg = "incorrect operator"
                    state = "error"
                    continue
                lex = ""
                state = "start"
        elif state == "string":
            if i != len(text) and text[i] != '"' and text[i] != "\n":
                lex += text[i]
                counter()
            else:
                if i != len(text) and text[i] == "\"":
                    lex += text[i]
                    const_table.add_row([lex, "string const"])
                    lex = ""
                    state = "start"
                    counter()
                else:
                    error_msg = "missing closing quote"
                    state = "error"
        elif state == "separator":
            lex = ""
            lex += text[i]
            if lex in delimeters:
                if (lex == ";"):
                    type = ""
                delimeter_table.add_row([lex, "separator"])
                lex = ""
                state = "start"
                counter()
            else:
                error_msg = "unsupported token"
                state = "error"
        elif state == "error":
            print(f"line: {line}, pos: {pos}. {error_msg}: {lex}")
            lex = ""
            break
        elif state == "end":
            print(keyword_table)
            print(variable_table)
            print(delimeter_table)
            print(operator_table)
            print(const_table)
            break
    