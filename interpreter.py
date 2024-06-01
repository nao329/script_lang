from parser_1 import String
from parser_1 import Variable
from parser_1 import Assignment
from parser_1 import Display
from parser_1 import If
from parser_1 import Repeat
from parser_1 import FunctionCall
from parser_1 import FunctionDef
from parser_1 import Return
from parser_1 import Program
from parser_1 import Number
from env import Environment


def evaluate(node, env):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, String):
        return node.value
    elif isinstance(node, Variable):
        # env.set_var(node.name, node.value)
        return env.variables.get(node.name, None)
    elif isinstance(node, Assignment):
        value = evaluate(node.value, env)
        env.set_var(node.variable.name, value)
        return value
    elif isinstance(node, Display):
        value = evaluate(node.value, env)
        print(value)
        return value
    elif isinstance(node, If):
        condition = evaluate(node.condition, env)
        if condition:
            return evaluate(node.then_branch, env)
        elif node.else_branch:
            return evaluate(node.else_branch, env)
    elif isinstance(node, Repeat):
        times = evaluate(node.times, env)
        for _ in range(times):
            evaluate(node.body, env)
    elif isinstance(node, FunctionDef):
        env.functions[node.name] = node
    elif isinstance(node, FunctionCall):
        func = env.functions.get(node.name)
        if func:
            local_env = Environment()
            local_env.variables = env.variables.copy()
            for param, arg in zip(func.params, node.args):
                local_env.variables[param] = evaluate(arg, env)
            result = None
            for stmt in func.body:
                result = evaluate(stmt, local_env)
            return result
    elif isinstance(node, Return):
        return evaluate(node.value, env)
    elif isinstance(node, Program):
        for statement in node.statements:
            evaluate(statement, env)
    else:
        raise TypeError(f'Unknown node type: {type(node)}')
