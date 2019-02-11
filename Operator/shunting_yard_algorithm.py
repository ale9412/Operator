import re


def is_number(token):
    try:
        int(token)
        return True
    except ValueError:
        return False


def greater_priority(op1, op2):
    precedences = {'+': 0, '-': 0, '*': 1, '/': 1}
    return precedences[op1] >= precedences[op2]


def get_top(stack):
    return stack[-1] if stack else None


def apply_operator(operators, values):
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
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = get_top(operators)
            while top is not None and top != "(":
                apply_operator(operators, values)
                top = peek(operators)
            operators.pop()
        else:
            top = get_top(operators)
            while top is not None and top not in "()" and greater_priority(top, token):
                apply_operator(operators, values)
                top = get_top(operators)
            operators.append(token)
    while get_top(operators) is not None:
        apply_operator(operators, values)
    return values[0]

