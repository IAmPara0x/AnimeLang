from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lg = LexerGenerator()

    def add_token(self, token_name: str, regex_token_val):
        self.lg.add(token_name, regex_token_val)

    def add_tokens(self, tokens_dict: dict) -> None:
        for token_name in tokens_dict.keys():
            self.lg.add(token_name, tokens_dict[token_name])

    def add_ignore(self, regex_val) -> None:
        self.lg.ignore(regex_val)

    def get_lexer(self):
        return self.lg.build()
