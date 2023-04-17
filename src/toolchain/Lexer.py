import re
from .Tokens import *
from .Errors import Err
        

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_pos = 0
        self.current_char = self.source_code[self.current_pos]
        self.line=1
        self.column=1
        self.error=False

    def advance(self):
        self.current_pos += 1
        self.column+=1
        if self.current_pos >= len(self.source_code):
            self.current_char = None
        else:
            self.current_char = self.source_code[self.current_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def tokenize_identifier(self):
        value = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_' or self.current_char == "."):
            value += self.current_char
            self.advance()
        return Token(TokenType.IDENTIFIER, value, self.line, self.column)

    def tokenize_number(self):
        value = ''
        while self.current_char is not None and self.current_char.isdigit():
            value += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, str(value), self.line, self.column)

    def tokenize_string(self):
        start_pos = self.current_pos
        self.current_pos += 1
        escaped = False
        while self.current_pos < len(self.source_code):
            if escaped:
                escaped = False
            elif self.source_code[self.current_pos] == '\\':
                escaped = True
            elif self.source_code[self.current_pos] == '"':
                token_value = self.source_code[start_pos:self.current_pos+1]
                self.current_pos += 1
                self.current_char = self.source_code[self.current_pos] if self.current_pos < len(self.source_code) else None
                return Token(TokenType.STRING, token_value, self.line, self.column)
            self.current_pos += 1
        raise Exception("Unterminated string at position " + str(start_pos))
    
    def symbolEval(self, symbol):
        return Token(symbol[1], symbol[0], self.line, self.column)

    def opEval(self, op):
        return Token(op[1], op[0], self.line, self.column)

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char=="\n": 
                    self.line+=1
                    self.column=0
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return self.tokenize_number()
            elif self.current_char == '"':
                return self.tokenize_string()
            elif self.current_char.isalpha() or self.current_char == '_' or self.current_char == ".":
                identifier=self.tokenize_identifier()
                if (identifier.value in [keychar[0] for keychar in KEYWORDS]):
                    keyword = KEYWORDS[([keychar[0] for keychar in KEYWORDS]).index(identifier.value)]
                    self.advance()
                    return Token(keyword[1], keyword[0], self.line, self.column)
                else: return identifier
            elif (self.current_char in [symchar[0] for symchar in SYMBOLS]) or (self.current_char + str(self.peek()) in [symchar[0] for symchar in SYMBOLS]):
                for symbol in SYMBOLS:
                    if self.current_char + str(self.peek()) == symbol[0]:
                        self.advance()
                        self.advance()
                        return self.symbolEval(symbol)
                symbol = SYMBOLS[([symchar[0] for symchar in SYMBOLS]).index(self.current_char)]
                self.advance()
                return self.symbolEval(symbol)
            elif (self.current_char in [opchar[0] for opchar in OPERATORS]) or (self.current_char + str(self.peek()) in [opchar[0] for opchar in OPERATORS]):
                for op in OPERATORS:
                    if self.current_char + str(self.peek()) == op[0]:
                        self.advance()
                        self.advance()
                        return self.opEval(symbol)
                operator = OPERATORS[([opchar[0] for opchar in OPERATORS]).index(self.current_char)]
                self.advance()
                return self.opEval(operator)
            else:
                self.error=True
                Err.unknownchar(self.line, self.column, self.current_char, self.source_code.splitlines()[self.line-1])
                self.advance()
        return Token(TokenType.EOF, "", self.line, self.column)

    def peek(self):
        if self.current_pos + 1 >= len(self.source_code):
            return None
        else:
            return self.source_code[self.current_pos + 1]

    def tokenize(self):
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        if self.error: exit(1)
        return tokens
