import re
#### STORES ALL THE TERMINAL TOKENS NAME FOR ANIME LANG ######

TOKENS_DICT = {}

# DATATYPES
TOKENS_DICT["FLOAT"] = r'[+-]?([0-9]+([.][0-9]*)|[.][0-9]+)'
TOKENS_DICT["INTEGER"] = r'([-+]?[0-9]+)'

# Operators
TOKENS_DICT["ADD"] = r'\+'
TOKENS_DICT["SUBSTRACT"] = r'\-'
TOKENS_DICT["DIVIDE"] = r'\/'
TOKENS_DICT["MULTIPLY"] = r'\*'

# symbols for evaluations
TOKENS_DICT["OPEN_PAREN"] = r'\('
TOKENS_DICT["CLOSE_PAREN"] = r'\)'
TOKENS_DICT["S_OPEN_PAREN"] = r'\['
TOKENS_DICT["S_CLOSE_PAREN"] = r'\]'
TOKENS_DICT["C_OPEN_PAREN"] = r'\{'
TOKENS_DICT["C_CLOSE_PAREN"] = r'\}'

# Keywords to create variables of different datatypes
TOKENS_DICT["INDEX_W"] = r'waifu'
TOKENS_DICT["NEW"] = r'new'
TOKENS_DICT["C_INTEGER"] = r'tsundere'
TOKENS_DICT["C_FLOAT"] = r'yandere'
TOKENS_DICT["EQUALS"] = r'='
TOKENS_DICT["C_LIST"] = r'harem'
TOKENS_DICT["COMMA"] = r','
TOKENS_DICT["C_BOOL"] = r'ship'
TOKENS_DICT["LINE_END"] = r'meow'
TOKENS_DICT["BAR"] = r'\|'
TOKENS_DICT["APPEND"] = r'ADD'
TOKENS_DICT["REMOVE"] = r'REMOVE'
TOKENS_DICT["TO"] = r'TO'
TOKENS_DICT["FROM"] = r'FROM'
TOKENS_DICT["SIZE"] = r'size'
TOKENS_DICT["TYPE"] = r'type'


# Keywords for conditionals
TOKENS_DICT["CHECK"] = r'create_ship'
TOKENS_DICT["ELSE"] = r'nani'
TOKENS_DICT["TRUE"] = r'kawai'
TOKENS_DICT["FALSE"] = r'baaka'
TOKENS_DICT["IS_EQUALS"] = r'X'

TOKENS_DICT["PRINT"] = r'moshi_moshi'
TOKENS_DICT["CLOSE"] = r'.exit'
TOKENS_DICT["VARIABLE"] = r'[a-zA-Z0-9_]+'
