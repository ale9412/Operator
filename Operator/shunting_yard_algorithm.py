import re


def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def greater_priority(op1, op2):
    precedences = {'+': 0, '-': 0, '*': 1, '/': 1}
    return precedences[op1] >= precedences[op2]


def get_top(stack):
    return stack[-1] if stack else None


def calculate(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()

    if operator == '+':
        result = float(left) + float(right)
    elif operator == '-':
        result = float(left) - float(right)
    elif operator == '*':
        result = float(left) * float(right)
    elif operator == '/':
        result = float(left) / float(right)

    values.append(result)



def evaluate(expression):
    tokens = re.findall(r"[+*/()-]|\d+", expression)
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(int(token))

        # This is in case parethesis exist in the operation
        # but to make the program a little faster I comment out
        # this section
        
##        elif token == '(':
##            operators.append(token)
##        elif token == ')':
##            top = get_top(operators)
##            while top is not None and top != "(":
##                calculate(operators, values)
##                top = peek(operators)
##            operators.pop()
        else:
            top = get_top(operators)
            while top is not None and greater_priority(top, token):
                calculate(operators, values)
                top = get_top(operators)
            operators.append(token)
    while get_top(operators) is not None:
        calculate(operators, values)
    return round(values[0],3)

