from env import Environment


env = Environment()


# parser.py
class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class String(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"

class Defined(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Defined({self.value})"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class Assignment(ASTNode):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def __repr__(self):
        return f"Assignment({self.variable}, {self.value})"

class Display(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Display({self.value})"

class If(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"

class Repeat(ASTNode):
    def __init__(self, times, body):
        self.times = times
        self.body = body

    def __repr__(self):
        return f"Repeat({self.times}, {self.body})"

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {self.params}, {self.body})"

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"

class Return(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

def parse(tokens):
    def parse_expression(index):
        token = tokens[index]
        if token[0] == 'NUMBER':
            return Number(token[1]), index + 1
        elif token[0] == 'STRING':
            return String(token[1]), index + 1
        elif token[0] == 'IDENTIFIER':
            return Variable(token[1]), index + 1
        raise SyntaxError('Invalid syntax: ' + str(token))

    def parse_assignment(index):
        if tokens[index][0] == 'VARIABLE':
            index += 1
            if tokens[index][0] == 'IDENTIFIER':
                variable = Variable(tokens[index][1])
                index += 1
                if tokens[index][0] == 'ASSIGN':
                    index += 1
                    value, index = parse_expression(index)
                    if tokens[index][0] == 'SET':
                        return Assignment(variable, value), index + 1
        raise SyntaxError('Invalid syntax in assignment')

    def parse_display(index):
        value, index = parse_expression(index)
        if tokens[index][0] == 'DISPLAY':
            return Display(value), index + 1
        raise SyntaxError('Invalid syntax in display')

    def parse_if(index):
        if tokens[index][0] == 'IF':
            index += 1
            var, index = parse_expression(index)
            print(var.name)
            if tokens[index][0] == "EQ":
                index += 1
                value2, index = parse_expression(index)
                value1 = env.get_var(var.name)
                print(value1)
                print(value2)
                condition = (value1 == value2.value)
                if tokens[index][0] == 'THEN':
                    index += 1
                    then_branch, index = parse_statement(index)
                    else_branch = None
                    if tokens[index][0] == 'ELSE':
                        index += 1
                        else_branch, index = parse_statement(index)
                    return If(condition, then_branch, else_branch), index
        raise SyntaxError('Invalid syntax in if statement')

    def parse_repeat(index):
        if tokens[index][0] == 'REPEAT':
            index += 1
            times, index = parse_expression(index)
            if tokens[index][0] == 'TIMES':
                index += 1
                body, index = parse_statement(index)
                return Repeat(times, body), index
        raise SyntaxError('Invalid syntax in repeat statement')

    def parse_function_def(index):
        if tokens[index][0] == 'FUNCTION':
            index += 1
            if tokens[index][0] == 'IDENTIFIER':
                name = tokens[index][1]
                index += 1
                if tokens[index][0] == 'LPAREN':
                    index += 1
                    params = []
                    while tokens[index][0] != 'RPAREN':
                        if tokens[index][0] == 'IDENTIFIER':
                            params.append(tokens[index][1])
                            index += 1
                        if tokens[index][0] == 'SEMICOLON':
                            index += 1
                    if tokens[index][0] == 'RPAREN':
                        index += 1
                        if tokens[index][0] == 'DEFINE':
                            index += 1
                            body, index = parse_block(index)
                            return FunctionDef(name, params, body), index
        raise SyntaxError('Invalid syntax in function definition')

    def parse_function_call(index):
        if tokens[index][0] == 'IDENTIFIER':
            name = tokens[index][1]
            index += 1
            if tokens[index][0] == 'LPAREN':
                index += 1
                args = []
                while tokens[index][0] != 'RPAREN':
                    arg, index = parse_expression(index)
                    args.append(arg)
                    if tokens[index][0] == 'SEMICOLON':
                        index += 1
                if tokens[index][0] == 'RPAREN':
                    return FunctionCall(name, args), index + 1
        raise SyntaxError('Invalid syntax in function call')

    def parse_statement(index):
        if tokens[index][0] == 'VARIABLE':
            return parse_assignment(index)
        elif tokens[index][0] == 'STRING' or tokens[index][0] == 'NUMBER' or tokens[index][0] == 'IDENTIFIER':
            return parse_display(index)
        elif tokens[index][0] == 'IF':
            return parse_if(index)
        elif tokens[index][0] == 'REPEAT':
            return parse_repeat(index)
        elif tokens[index][0] == 'FUNCTION':
            return parse_function_def(index)
        elif tokens[index][0] == 'IDENTIFIER':
            return parse_function_call(index)
        raise SyntaxError('Invalid statement syntax')

    def parse_block(index):
        statements = []
        while index < len(tokens) and tokens[index][0] != 'RBRACE':
            statement, index = parse_statement(index)
            statements.append(statement)
        return statements, index

    statements, _ = parse_block(0)
    return Program(statements)
