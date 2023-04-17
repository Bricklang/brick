from enum import Enum, auto
from collections import namedtuple


class TokenType(Enum):
    IDENTIFIER            = auto()
    NUMBER                = auto()
    OPERATOR              = auto()
    SYMBOL                = auto()
    STRING                = auto()


    EQUAL                 = auto()
    DCOLON                = auto()
    COLON                 = auto()
    RARROW                = auto()
    SEMICOLON             = auto()
    LPAREN                = auto()
    RPAREN                = auto()
    COMMA                 = auto()
    LBRACE                = auto()
    RBRACE                = auto()
    AND                   = auto()


    IF                    = auto()
    ELSE                  = auto()
    WHILE                 = auto()
    RETURN                = auto()


    PLUS                  = auto()
    MINUS                 = auto()
    MULTIPLY              = auto()
    DIVIDE                = auto()
    POW                   = auto()
    FLOOR                 = auto()
    INCREMENT             = auto()
    DECREMENT             = auto()
    GREATER_THAN          = auto()
    LESS_THAN             = auto()
    DEQUAL                = auto()
    NOT                   = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN_OR_EQUAL    = auto()


    EOF                   = auto()

SYMBOLS=[
    ["=",  TokenType.EQUAL],
    [";",  TokenType.SEMICOLON],
    ["::", TokenType.DCOLON],
    [":",  TokenType.COLON],
    ["->", TokenType.RARROW],
    ["(",  TokenType.LPAREN],
    [")",  TokenType.RPAREN],
    [",",  TokenType.COMMA],
    ["{",  TokenType.LBRACE],
    ["}",  TokenType.RBRACE],
    ["&",  TokenType.AND]
]

OPERATORS=[
    ["+",  TokenType.PLUS],
    ["-",  TokenType.MINUS],
    ["*",  TokenType.MULTIPLY],
    ["/",  TokenType.DIVIDE],
    ["**", TokenType.POW],
    ["++", TokenType.INCREMENT],
    ["--", TokenType.DECREMENT],
    ["//", TokenType.FLOOR],
    [">",  TokenType.GREATER_THAN],
    ["<",  TokenType.LESS_THAN],
    ["==", TokenType.DEQUAL],
    ["!=", TokenType.NOT],
    [">=", TokenType.GREATER_THAN_OR_EQUAL],
    ["<=", TokenType.LESS_THAN_OR_EQUAL]
]

KEYWORDS=[
    ["if",    TokenType.IF],
    ["else",  TokenType.ELSE],
    ["while", TokenType.WHILE],
    ["ret",   TokenType.RETURN]
]

Token = namedtuple("Token", ["type", "value", "line", "column"])