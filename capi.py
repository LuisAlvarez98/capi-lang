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
    'RUN','START','RETURN', 'LEFTHAT','RIGHTHAT','TRUE','FALSE','BOOL','TBOOL', 'COMMENT', 'VOID', 'DRAW', 'SIZE',
    "HEAD","TAIL","LAST","SET_TITLE","SET_COLOR","CREATE_OBJECT","CREATE_TEXT","SET_DIMENSION",'MAIN'
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
    'main' :'MAIN',
    'list':'TLIST',
    'print':'PRINT',
    'object': 'TOBJECT',
    'run': 'RUN',
    'start': 'START',
    'return': 'RETURN',
    'void': 'VOID',
    'draw':'DRAW',
    'size':'SIZE',
    'head':'HEAD',
    'tail':'TAIL',
    'last':'LAST',
    'set_title': 'SET_TITLE',
    'set_color': 'SET_COLOR',
    'create_object': 'CREATE_OBJECT',
    'create_text': 'CREATE_TEXT',
    'set_dimension': 'SET_DIMENSION'
}

func_dir = {'start': ['void', []],'run': ['void', []]}
global_vars = {}

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
    capi : global recfunc MAIN COLON LEFTKEY start RIGHTKEY SEMICOLON
         | recfunc MAIN COLON LEFTKEY start RIGHTKEY SEMICOLON
         | global MAIN COLON LEFTKEY start RIGHTKEY SEMICOLON
         | MAIN COLON LEFTKEY start RIGHTKEY SEMICOLON
    '''

def p_global(p):
    '''
    global : GLOBAL COLON LEFTKEY vars RIGHTKEY SEMICOLON
    '''
    for v in p[4]:
        v.append('global')
        if v[0] in global_vars.keys():
            print("Variable already exists in global.") #throw error
        else:
            global_vars[v[0]] = [v[1],v[2]]
    
    
def p_start(p):
    '''
    start : VOID FUNC START LEFTPAR RIGHTPAR block run
    '''
    var_func_dict = {} # dictionary used for function scope
    if p[6] is not None:
        for v in p[6]:
            v.append(p[3])
            if v[0] in var_func_dict.keys():
                print("Variable already exists in func.") #throw error
            else:
                var_func_dict[v[0]] = [v[1],v[2]]

    func_dir['start'].append(var_func_dict)
    print(func_dir)
    
def p_run(p):
    '''
    run : VOID FUNC RUN LEFTPAR RIGHTPAR block
    '''
    var_func_dict = {} # dictionary used for function scope
    if p[6] is not None:
        for v in p[6]:
            v.append(p[3])
            if v[0] in var_func_dict.keys():
                print("Variable already exists in func.") #throw error
            else:
                var_func_dict[v[0]] = [v[1],v[2]]

    func_dir['run'].append(var_func_dict)
    print(func_dir)

def p_vars(p): 
    ''' 
    vars :    VAR recids COLON type EQUAL expression SEMICOLON vars 
            | VAR recids COLON type EQUAL expression SEMICOLON
            | VAR recids COLON type SEMICOLON vars
            | VAR recids COLON type SEMICOLON
    '''
    rule_len = len(p) - 1
    var_list = []

    if type(p[2]) == list:
        for l in p[2]:
            var_list.append([l, p[4]])
    else:
        var_list.append([p[2],p[4]])

    if rule_len == 8: 
        var_list = var_list + p[8]
    elif rule_len == 6: 
        var_list = var_list + p[6]
    
    p[0] = var_list
    
def p_recids(p):  
    ''' 
    recids : ID 
           | ID COMMA recids 
    '''
    rule_len = len(p) - 1
    if rule_len == 1:
        p[0] = p[1]
    elif rule_len == 3:
        p[0] = [p[1]] + [p[3]]

def p_block(p):
    '''
    block : COLON LEFTKEY recstatement RIGHTKEY SEMICOLON
          | COLON LEFTKEY RIGHTKEY SEMICOLON
    '''
    # in this case we just send the statements when the rule length is 5
    rule_len = len(p) - 1
    if rule_len == 5:
        p[0] = p[3]

def p_recstatement(p):
    ''' 
    recstatement : statement recstatement  
                 | statement  
    '''
    # this currently works just for one statement
    p[0] = p[1]

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
              | specialfunction SEMICOLON
    '''
    # in here we are sending the first instruction of our grammar
    p[0] = p[1]

def p_specialfunction(p):
    '''
    specialfunction : draw
                    | size
                    | head
                    | tail
                    | last
                    | set_title
                    | set_dimension
                    | set_color
                    | create_object
                    | create_text
    '''

def p_draw(p):
    '''
    draw : DRAW LEFTPAR recfuncexp RIGHTPAR
        
    '''

def p_size(p):
    '''
    size : SIZE LEFTPAR RIGHTPAR
    '''

def p_head(p):
    '''
    head : HEAD LEFTPAR RIGHTPAR
    '''

def p_tail(p):
    '''
    tail : TAIL LEFTPAR RIGHTPAR
    '''

def p_last(p):
    '''
    last : LAST LEFTPAR RIGHTPAR
    '''

def p_set_title(p):
    '''
    set_title : SET_TITLE LEFTPAR expression RIGHTPAR
    '''

def p_set_dimension(p):
    '''
    set_dimension : SET_DIMENSION LEFTPAR expression COMMA expression RIGHTPAR
    '''

def p_set_color(p):
    '''
    set_color : SET_COLOR LEFTPAR expression COMMA expression COMMA expression RIGHTPAR
    '''

def p_create_object(p):
    '''
    create_object : CREATE_OBJECT LEFTPAR recfuncexp RIGHTPAR
    '''

def p_create_text(p):
    '''
    create_text : CREATE_TEXT LEFTPAR recfuncexp RIGHTPAR
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
    for : FOR LEFTPAR assign SEMICOLON expression SEMICOLON assign SEMICOLON RIGHTPAR block
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
    rule_len = len(p) - 1
    params = [] # array used for funciton params

    var_func_dict = {} # dictionary used for function scope

    if rule_len == 7:
        for v in p[7]:
            v.append(p[3])
            if v[0] in var_func_dict.keys():
                print("Variable already exists in func.") #throw error
            else:
                var_func_dict[v[0]] = [v[1],v[2]]

        params = p[5]
    elif rule_len == 6:
        for v in p[6]:
            v.append(p[3])
            if v[0] in var_func_dict.keys():
                print("Variable already exists in func.") #throw error
            else:
                var_func_dict[v[0]] = [v[1],v[2]]
        params = []  
   
    if p[3] in func_dir.keys():
       print("Function name already exists.") 
    else:
       func_dir[p[3]] = [p[1], params,var_func_dict]

    print(func_dir)
 

def p_recparams(p):
    '''
    recparams : ID COLON type
              | ID COLON type COMMA recparams
    '''
    rule_len = len(p) - 1
    if rule_len == 3:
        p[0] = [(p[1],p[3])]
    elif rule_len  == 5:
        p[0] = [(p[1],p[3])] + p[5]


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
    p[0] = p[1]

def p_primitivetype(p):
    '''
    primitivetype : TINT
                  | TFLOAT
                  | TSTRING
                  | TBOOL
                  | TOBJECT
    '''
    p[0] = p[1]

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
        | specialfunction
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
