#------------------------------------------------------
# Capi Lang
# lex.py
# 
# By:
# Luis Felipe Alvarez & David Cantu Martinez
#
#------------------------------------------------------
import ply.lex as lex

tokens = (
    'ID','IF','ELSE','EX','TERM','RELOP','LOGIC','LEFTPAR','RIGHTPAR',
    'LEFTKEY','RIGHTKEY','LEFTBRACKET','RIGHTBRACKET','EQUALS','SEMCOLON',
    'COLON','COMMA','VAR','TINT','TFLOAT','TSTRING','INT','FLOAT','STRING',
    'FOR','FUNC','WHILE','GLOBAL','LIST','TLIST','OBJECT','DOT','SCENE','PRINT',
    'RUN','START'
)

reserved = {
    'int':'TINT',
    'float':'TFLOAT',
    'string':'TSTRING',
    'if':'IF',
    'else':'ELSE',
    'var':'VAR',
    'for':'FOR',
    'while':'WHILE',
    'global':'GLOBAL',
    'func':'FUNC',
    'list':'TLIST',
    'print':'PRINT',
    'object': 'OBJECT',
    'scene':'SCENE',
    'run': 'RUN',
    'start': 'START'
}

t_RELOP = r'[\< | \> | \<\> | \=\< | \>\=]'
t_LOGIC = r'[\|\| | \&\&]'
t_EX = r'[\+|\-]'
t_TERM = r'[\*|\/]'
t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_LEFTKEY = r'\{'
t_RIGHTKEY = r'\}'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_EQUALS  = r'\='
t_SEMCOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    print(t)
    return t 

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"[a-zA-Z_][a-zA-Z0-9_]*\"'
    return t


# Ignored characters (TO DO comments //)
t_ignore = " \t\r\n\f\v"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.type = 'ID'
    return t    

def t_error(t):
    print(t)
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lex = lex.lex()
print(lex)