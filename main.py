# main.py
from lexer import tokenize
from parser_1 import parse
from interpreter import Environment, evaluate


def main():
    code = """
    変数 x を 5 に設定。
    x を表示
    """
    tokens = tokenize(code)
    print("Tokens:", tokens)
    ast = parse(tokens)
    print("AST:", ast)
    env = Environment()
    evaluate(ast, env)

if __name__ == '__main__':
    main()
