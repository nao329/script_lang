import re

TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+'),
    ('STRING', r'"[^"]*"'),
    ('SET', r'に設定'),
    ('VARIABLE', r'変数'),
    ('DISPLAY', r'を表示'),
    ('MESSAGE', r'メッセージ'),
    ('IF', r'もし'),
    ('THEN', r'ならば'),
    ('ELSE', r'それ以外ならば'),
    ('TIMES', r'回'),
    ('REPEAT', r'繰り返し'),
    ('FUNCTION', r'関数'),
    ('DEFINE', r'を定義し'),
    ('RETURN', r'を返す'),
    ('ASSIGN', r'を'),
    ('LPAREN', r'（'),
    ('RPAREN', r'）'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r'、'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('EQ', r'が'),
    ('SKIP', r'[ 。\t\n]+'),
    ('IDENTIFIER', r'[一-龥ぁ-んァ-ヶa-zA-Z_]+'),
    ('MISMATCH', r'.')
]

def tokenize(code):
    tokens = []
    for mo in re.finditer('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION), code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'STRING':
            value = value.strip('"')
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        tokens.append((kind, value))
    return tokens
