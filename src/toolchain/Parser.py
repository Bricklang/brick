from .Tokens import *
from .Colors import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ptokens = []+tokens
        self.current_token = None
        self.tokenpos=0
        self.line = 1
        self.column = 1
        self.ast=({"program": []})
        self.tree=self.ast["program"]
    
    def parse(self):
        self.advance()
        return self.statement()
    
    def advance(self):
        if len(self.tokens) > 0:
            self.current_token = self.tokens.pop(0)
            self.line = self.current_token.line
            self.column = self.current_token.column + len(self.current_token.value)
            self.tokenpos+=1

    def peek(self, i:int=1):
        return self.ptokens[self.tokenpos+i]
    
    def beff(self, i:int=1):
        return self.ptokens[self.tokenpos-i]
    
    def need(self, token_type, token_value=None):
        if self.current_token.type != token_type:
            raise Exception(f"Expected {token_type} at line {self.line}, column {self.column}")
        if token_value is not None and self.current_token.value != token_value:
            raise Exception(f"Expected {token_value} at line {self.line}, column {self.column}")
        self.advance()
    
    def parse_function(self):
        self.need(TokenType.IDENTIFIER, "fn")
        name = self.current_token.value
        self.need(TokenType.IDENTIFIER)
        self.need(TokenType.LPAREN)
        parameters = []
        while self.current_token.type != TokenType.RPAREN:
            param_name = self.current_token.value
            self.need(TokenType.IDENTIFIER)
            self.need(TokenType.DCOLON)
            param_type = self.current_token.value
            self.need(TokenType.IDENTIFIER)
            parameters.append((param_name, param_type))
            if self.current_token.type == TokenType.COMMA:
                self.advance()
        self.need(TokenType.RPAREN)
        self.need(TokenType.RARROW)
        return_type = self.current_token.value
        self.need(TokenType.IDENTIFIER)
        self.need(TokenType.LBRACE)
        statements = self.parse_statements()
        self.need(TokenType.RBRACE)
        self.tree.append(
            {
                "stat_name": "fn_def",
                "name": name,
                "type": return_type,
                "parameters": parameters,
                "statements": statements
            }
        )

    def expression(self):
        left = self.term()
        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.term()
            left = {
                "operator": operator,
                "left": left,
                "right": right
            }
        return left

    def term(self):
        left = self.factor()
        while self.current_token is not None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.value
            self.advance()
            right = self.factor()
            left = {
                "operator": operator,
                "left": left,
                "right": right
            }
        return left

    def factor(self):
        if self.current_token.type == TokenType.NUMBER:
            result = {
                "term": self.current_token.value
            }
            self.advance()
            return result
        elif self.current_token.type == TokenType.STRING:
            result = {
                "term": self.current_token.value
            }
            self.advance()
            return result
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            result = {
                "parenthesized": self.expression()
            }
            self.need(TokenType.RPAREN)
            return result
        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            if self.current_token.type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.current_token.type != TokenType.RPAREN:
                    args.append(self.expression())
                    if self.current_token.type == TokenType.COMMA:
                        self.advance()
                self.need(TokenType.RPAREN)
                result = {
                    "function_call": {
                        "name": name,
                        "args": args
                    }
                }
                return result
            else:
                result = {
                    "identifier": name
                }
                return result
        elif self.current_token.type == TokenType.MINUS:
            self.advance()
            result = {
                "unary_minus": self.factor()
            }
            return result
        elif self.current_token.type == TokenType.NOT:
            self.advance()
            result = {
                "not": self.factor()
            }
            return result

    
    def condition(self):
        left = self.expression()
        if self.current_token.type == TokenType.EQUAL:
            self.advance()
            right = self.expression()
            return left == right
        elif self.current_token.type == TokenType.LESS_THAN:
            self.advance()
            right = self.expression()
            return left < right
        elif self.current_token.type == TokenType.GREATER_THAN:
            self.advance()
            right = self.expression()
            return left > right
        else:
            raise RuntimeError('Invalid comparison operator')
    
    def if_statement(self):
        self.advance()
        condition = self.condition()
        if self.current_token.type == TokenType.COLON:
            self.advance()
            if condition:
                self.statement()
            if self.current_token.type == TokenType.ELSE:
                self.advance()
                self.statement()
        else:
            raise RuntimeError('Missing colon after if statement')

    def parse_return(self):
        self.need(TokenType.RETURN, "ret")
        exp = self.expression()
        self.need(TokenType.SEMICOLON)
        return (
            {
                "stat_name": "ret_stat",
                "expression": exp
            }
        )

    def call_function(self):
        name=self.current_token.value
        self.advance()
        self.need(TokenType.LPAREN)
        args = []
        while self.current_token.type != TokenType.RPAREN:
            param_name = self.expression()
            args.append(param_name)
            if self.current_token.type == TokenType.COMMA:
                self.advance()
        self.need(TokenType.RPAREN)
        self.need(TokenType.SEMICOLON)
        return {
            "stat_name": "func_call",
            "name": name,
            "args": args
        }

    def parse_variable(self):
        self.need(TokenType.IDENTIFIER, "val")
        name=self.current_token.value
        self.advance()
        self.need(TokenType.DCOLON)
        vtype=self.current_token.value
        self.advance()
        value=None
        if (self.current_token == TokenType.EQUAL):
            self.advance()
            value=self.current_token.value
        self.need(TokenType.SEMICOLON)
        return {
            "stat_name": "var_def",
            "name": name,
            "type": vtype,
            "value": value
        }

    def parse_statements(self):
        statements = []
        i=0
        while self.current_token.type != TokenType.RBRACE:
            statements.append(self.stat())
            i+=1
        return statements

    def stat(self):
        if self.current_token.type == TokenType.RETURN:
            return self.parse_return()
        elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "val":
            return self.parse_variable()

        #### ALWAYS THE LAST IN THE ORDER BECAUSE IT'S VERY GENERIC
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.call_function()
        else:
            raise Exception(f"Invalid statement at line {self.line}, column {self.column}")

    def statement(self):
        if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "fn":
            return self.parse_function()
        elif self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "val":
            return self.parse_variable()
        else:
            raise Exception(f"Invalid statement at line {self.line}, column {self.column}")