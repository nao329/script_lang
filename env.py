class Environment:
    def __init__(self):
        self.variables = {}

    def set_var(self, name, value):
        self.variables[name] = value

    def get_var(self, name):
        return self.variables.get(name, None)


# グローバルな環境インスタンスを作成
global_env = Environment()
