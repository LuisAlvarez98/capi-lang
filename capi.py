#------------------------------------------------------
# Capi Lang
# capi.py
# 
# By:
# Luis Felipe Alvarez & David Cantu Martinez
#
#------------------------------------------------------
import ply.lex as lex

tokens = (
    'ID','IF','ELSE','EX','TERMS','RELOP','LOGIC','LEFTPAR','RIGHTPAR',
    'LEFTKEY','RIGHTKEY','LEFTBRACKET','RIGHTBRACKET','EQUAL','SEMICOLON',
    'COLON','COMMA','VAR','TINT','TFLOAT','TSTRING','INT','FLOAT','STRING',
    'FOR','FUNC','WHILE','GLOBAL','LIST','TLIST','OBJECT','TOBJECT','DOT','PRINT',
    'RUN','START','RETURN', 'LEFTHAT','RIGHTHAT','TRUE','FALSE','BOOL','TBOOL', 'COMMENT', 'VOID'
)

reserved = {
    'int':'TINT',
    'float':'TFLOAT',
    'bool' : 'TBOOL',
    'string':'TSTRING',
    'true':'TRUE',
    'false':'FALSE',
    'if':'IF',
    'else':'ELSE',
    'var':'VAR',
    'for':'FOR',
    'while':'WHILE',
    'global':'GLOBAL',
    'func':'FUNC',
    'list':'TLIST',
    'print':'PRINT',
    'object': 'TOBJECT',
    'run': 'RUN',
    'start': 'START',
    'return': 'RETURN',
    'void': 'VOID',
}

t_EQUAL  = r'\='
t_RELOP = r'\<\=|\>\=|\>|\<|\!\=|\=\='
t_LOGIC = r'\|\| | \&\&'
t_EX = r'\+|\-'
t_TERMS = r'\*|\/'
t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_LEFTKEY = r'\{'
t_RIGHTKEY = r'\}'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_LEFTHAT = r'\<'
t_RIGHTHAT = r'\>'

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
    r'\"[a-zA-Z_ ][a-zA-Z0-9_ ]*\"'
    return t

def t_TRUE(t):
    r'(true)'
    t.value = True
    return t

def t_FALSE(t):
    r'(false)'
    t.value = False
    return t

def t_COMMENT(t):
    r'\@.*'
    pass
    # No return value. Token discarded

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

#Program
def p_capi(p):
    ''' 
    capi : global recfunc 
         | recfunc
    '''

def p_global(p):
    '''
    global : GLOBAL COLON LEFTKEY vars RIGHTKEY SEMICOLON
    '''

def p_vars(p): 
    ''' 
    vars : VAR recvars 
    '''

def p_recvars(p): 
    ''' 
    recvars : recids COLON type EQUAL expression SEMICOLON vars 
            | recids COLON type EQUAL expression SEMICOLON
            | recids COLON type SEMICOLON vars
            | recids COLON type SEMICOLON
    '''

def p_recids(p):  
    ''' 
    recids : ID 
           | ID COMMA recids 
    '''

def p_block(p):
    '''
    block : COLON LEFTKEY recstatement RIGHTKEY SEMICOLON
          | COLON LEFTKEY RIGHTKEY SEMICOLON
    '''
    
def p_recstatement(p):
    ''' 
    recstatement : statement recstatement  
                 | statement  
    '''

def p_statement(p):
    '''
    statement : assign SEMICOLON
              | condition
              | vars
              | loop
              | write SEMICOLON
              | return SEMICOLON
              | functioncall SEMICOLON
              | nestedassign SEMICOLON
    '''
    
def p_assign(p):
    '''
    assign : ID EQUAL expression
    '''

def p_condition(p):
    ''' condition : IF LEFTPAR expression RIGHTPAR block 
                  | IF LEFTPAR expression RIGHTPAR block ELSE block 
     '''
     
def p_loop(p):
    '''
    loop : for
        | while
    '''
def p_for(p):
    '''
    for : FOR LEFTPAR assign SEMICOLON expression SEMICOLON expression SEMICOLON RIGHTPAR block
    '''
def p_while(p):
    '''
    while : WHILE LEFTPAR expression RIGHTPAR block
    '''

def p_function(p):
    '''
    function : type FUNC ID LEFTPAR recparams RIGHTPAR block
             | type FUNC ID LEFTPAR RIGHTPAR block
             | VOID FUNC ID LEFTPAR recparams RIGHTPAR block
             | VOID FUNC ID LEFTPAR RIGHTPAR block
    '''

def p_recparams(p):
    '''
    recparams : ID COLON type
              | ID COLON type COMMA recparams
    '''
def p_recfunc(p):
    '''
    recfunc : function recfunc
            | function
    '''  
    
def p_write(p):
    ''' 
    write : PRINT LEFTPAR recwrite RIGHTPAR 
    '''
    
def p_recwrite(p):
    ''' 
    recwrite : expression COMMA recwrite 
               | STRING COMMA recwrite 
               | expression 
               | STRING
    '''

def p_return(p):
    '''
     return : RETURN expression
    '''

def p_functioncall(p):
    '''
    functioncall : ID LEFTPAR recfuncexp RIGHTPAR 
                 | ID LEFTPAR RIGHTPAR 
    '''

def p_recfuncexp(p):
    '''
    recfuncexp : expression COMMA recfuncexp
               | expression 
    '''

def p_expression(p):
    '''
    expression : exp RELOP exp
               | exp LOGIC exp
               | exp
    '''
    
def p_exp(p):
    ''' 
    exp : term recexp
        | term 
        '''

def p_recexp(p):
    ''' 
    recexp : EX exp 
    '''

def p_term(p):
    ''' 
    term : factor recterm 
            | factor 
    '''

def p_recterm(p):
    ''' 
    recterm : TERMS term
    '''

def p_factor(p): 
    ''' factor : LEFTPAR expression RIGHTPAR 
               | EX cte
               | cte
    '''

def p_type(p):
    '''
    type : primitivetype
        | LIST LEFTHAT primitivetype RIGHTHAT
    '''

def p_primitivetype(p):
    '''
    primitivetype : TINT
                  | TFLOAT
                  | TSTRING
                  | TBOOL
                  | TOBJECT
    '''

def p_listaccess(p):
    '''
    listaccess : ID LEFTBRACKET expression RIGHTBRACKET SEMICOLON
    '''

def p_nestedvalue(p):
    '''
    nestedvalue : ID DOT ID
    '''

def p_nestedassign(p):
    '''
    nestedassign : nestedvalue EQUAL expression
    '''

def p_cte(p):
    '''
    cte : STRING 
        | ID
        | INT
        | FLOAT
        | BOOL
        | nestedvalue
        | functioncall
        | listaccess
    '''
def p_error(p):
    print("ERROR {}".format(p))
    print(f"Syntax error at {p.value!r}")
    exit()
    
import ply.yacc as yacc
yacc.yacc()

f = open('code.capi')
s = f.read()
f.close()

yacc.parse(s)

print('Code is okay.')
