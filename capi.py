#------------------------------------------------------
# Capi Lang
# capi.py
# 
# By:
# Luis Felipe Alvarez & David Cantu Martinez
#
#------------------------------------------------------
import ply.lex as lex
from collections import deque #Para el stack de scopes
from semantic_cube import *
from util import get_type, get_type_s

# Inits the semantic cube
s_cube = semantic_cube()

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

temporals = 0


class quadruple():
    def __init__(self, operator, left_operand, right_operand, temp):
        self.id = -1
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.temp = temp
    def __str__(self):
        return f'operator: {self.operator}, left_operand: {self.left_operand}, right_operand: {self.right_operand}, temp: {self.temp}\n'
    def __repr__(self):
        return f'operator: {self.operator}, left_operand: {self.left_operand}, right_operand: {self.right_operand}, temp: {self.temp}\n'

class variable():
    def __init__(self, varid, vartype):
        self.id = varid
        self.type = vartype
    def __str__(self):
        return f'Id: {self.id}, Type: {self.type}'
    def __repr__(self):
        return f'Id: {self.id}, Type: {self.type}'

class function_values():
    def __init__(self, functiontype='', params=[], scopevars={}):
        self.functiontype = functiontype
        self.params = params.copy()
        self.vars = scopevars.copy()

    def __str__(self):
        return f'Type: {self.functiontype}, Params: {self.params}, Vars: {self.vars}\n'
    def __repr__(self):
        return f'Type: {self.functiontype}, Params: {self.params}, Vars: {self.vars}\n'


def get_next_avail():
    global temporals
    temporals = temporals + 1
    return "t" + str(temporals)

quadruples = [] #Lista de cuadruplos
operator_stack = deque() # Stack de operadores + - * /
operand_stack = deque() # Stack de operandos variables 
types_stack = deque() #Stack de tipos int, float
go_to_stack = deque() #Stack de saltos

# Function Directory
func_dir = {}
active_scopes = deque() #Stack de scopes
active_scopes.append(function_values('global', [], {}))


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

relop_arr = ['<=',">=",">","<","!=","=="]
logic_arr = ["||","&&"]

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
    capi : global recfunc MAIN COLON LEFTKEY start run RIGHTKEY SEMICOLON
         | recfunc MAIN COLON LEFTKEY start run RIGHTKEY SEMICOLON
         | global MAIN COLON LEFTKEY start run RIGHTKEY SEMICOLON
         | MAIN COLON LEFTKEY start run RIGHTKEY SEMICOLON
    '''
    print(quadruples)

def p_global(p):
    '''
    global : GLOBAL COLON LEFTKEY vars RIGHTKEY SEMICOLON
    '''
    globalscope = active_scopes.pop()
    func_dir['global'] = globalscope
    active_scopes.append(globalscope)

    
def p_start(p):
    '''
    start : VOID FUNC START startscope_action LEFTPAR RIGHTPAR block 
    '''
    new_func = active_scopes.pop()
    new_func.functiontype =  'void'
    new_func.params = []
    
    func_dir[p[3]] = new_func
    
def p_run(p):
    '''
    run : VOID FUNC RUN  startscope_action LEFTPAR RIGHTPAR block
    '''
    new_func = active_scopes.pop()
    new_func.functiontype =  'void'
    new_func.params = []
    
    func_dir[p[3]] = new_func


def p_vars(p): 
    ''' 
    vars :    VAR recids COLON type EQUAL expression SEMICOLON vars 
            | VAR recids COLON type EQUAL expression SEMICOLON
            | VAR recids COLON type SEMICOLON vars
            | VAR recids COLON type SEMICOLON
    '''
    rule_len = len(p) - 1
    #print(active_scopes)
    current_function = active_scopes.pop()

    for l in p[2]:
        current_function.vars[l] = variable(l,p[4])
    
    active_scopes.append(current_function)
def p_recids(p):  
    ''' 
    recids : ID 
           | ID COMMA recids 
    '''
    rule_len = len(p) - 1
    if rule_len == 1:
        p[0] = [p[1]]
    elif rule_len == 3:
        p[0] = [p[1]] + [p[3]]

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
    # this currently works just for one statement

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
    assign : ID assign_action1 EQUAL assign_action2 expression 
    '''
    # we need to do the same for var i :int = 5;
    result = operand_stack.pop()
    type_result = types_stack.pop()
    if len(operand_stack) > 0:
        left_operand = operand_stack.pop()
        left_operand_type = types_stack.pop()
        operator = operator_stack.pop()

        expression_type = s_cube.validate_expression(type_result, left_operand_type, operator)
        if expression_type != "ERROR":
            quadruples.append(quadruple(operator, result, None, left_operand))
            

def p_assign_action1(p):
    '''
    assign_action1 : 
    '''
    current_id = p[-1] #get current ID
    current_active_scopes = active_scopes.copy()
    current_type = ""
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if current_id in current_vars:
            current_type = current_vars[current_id].type
            break
        current_active_scopes.pop()
    
    if(len(current_active_scopes) <= 0):
        print("Variable does not exist!")
    else:
        operand_stack.append(current_id)
        types_stack.append(get_type_s(current_type))


def p_assign_action2(p):
    '''
    assign_action2 : 
    '''
    operator_stack.append(p[-1])


def p_condition(p):
    ''' condition : IF startscope_action LEFTPAR expression condition_action1 RIGHTPAR  block condition_action2
                  | IF startscope_action LEFTPAR expression condition_action1 RIGHTPAR  block condition_action3 ELSE  block condition_action2
     '''
    new_func = active_scopes.pop() # Get the last function created
    new_func.functiontype =  ""  # Assign a name to the function
    new_func.params = []
     
def p_condition_action1(p):
    '''
    condition_action1 :
    '''
    exp_type = types_stack.pop()
    if exp_type != "b":
        print("Error, Type Mismatch") 
    else:
        result = operand_stack.pop()
        quadruples.append(quadruple("GOTO_F", result,None,None))
        go_to_stack.append(len(quadruples)-1)
        
def p_condition_action2(p):
    '''
    condition_action2 :
    '''
    jump = go_to_stack.pop()
    quadruples[jump] = quadruple(quadruples[jump].operator, quadruples[jump].left_operand,None, len(quadruples))
    
def p_condition_action3(p):
    '''
    condition_action3 :
    '''
    false = go_to_stack.pop()
    quadruples.append(quadruple("GOTO", None,None,None))
    go_to_stack.append(len(quadruples) - 1)
    quadruples[false] = quadruple("GOTO_F",quadruples[false].left_operand,None,len(quadruples))

def p_loop(p):
    '''
    loop : for
        | while
    '''

def p_for(p):
    '''
    for : FOR startscope_action LEFTPAR  assign  SEMICOLON for_action1 expression for_action2 SEMICOLON  assign  SEMICOLON RIGHTPAR block for_action3
    '''
    new_func = active_scopes.pop() # Get the last function created
    new_func.functiontype =  ""  # Assign a name to the function
    new_func.params = []

def p_for_action1(p):
    '''
    for_action1 : 
    '''
    go_to_stack.append(len(quadruples))

def p_for_action2(p):
    '''
    for_action2 : 
    '''
    print(operand_stack)
    print(operator_stack)
    cond = operand_stack.pop()
    cond_type = types_stack.pop()

    if cond_type != "b":
        print("Error, Type Mismatch") 
    else:
        quadruples.append(quadruple("GOTO_F", cond,None,None))
        go_to_stack.append(len(quadruples)-1)
        
def p_for_action3(p):
    '''
    for_action3 : 
    '''
    falso = go_to_stack.pop() 
    ref = go_to_stack.pop()
    quadruples.append(quadruple("GOTO", None, None, ref))
    quadruples[falso] = quadruple(quadruples[falso].operator, quadruples[falso].left_operand,None, len(quadruples))
    
    
def p_while(p):
    '''
    while : WHILE startscope_action while_action1 LEFTPAR expression while_action2 RIGHTPAR block while_action3
    '''
    new_func = active_scopes.pop() # Get the last function created
    new_func.functiontype =  ""  # Assign a name to the function
    new_func.params = []

    print(go_to_stack)

def p_while_action1(p):
    '''
    while_action1 :
    '''
    go_to_stack.append(len(quadruples))

def p_while_action2(p):
    '''
    while_action2 :
    '''
    cond = operand_stack.pop()
    cond_type = types_stack.pop()

    if cond_type != "b":
        print("Error, Type Mismatch") 
    else:
        quadruples.append(quadruple("GOTO_F", cond,None,None))
        go_to_stack.append(len(quadruples)-1)

def p_while_action3(p):
    '''
    while_action3 :
    '''
    falso = go_to_stack.pop() 
    ref = go_to_stack.pop()
    quadruples.append(quadruple("GOTO", None, None, ref))
    quadruples[falso] = quadruple(quadruples[falso].operator, quadruples[falso].left_operand,None, len(quadruples))

def p_function(p):
    '''
    function : type FUNC ID startscope_action LEFTPAR recparams RIGHTPAR block
             | type FUNC ID startscope_action LEFTPAR RIGHTPAR block
             | VOID FUNC ID startscope_action LEFTPAR recparams RIGHTPAR block
             | VOID FUNC ID startscope_action LEFTPAR RIGHTPAR block
    '''
    rule_len = len(p) - 1
    params = [] # array used for funciton params


    if rule_len == 8:
        params = p[6]
    elif rule_len == 7:
        params = []  
   
    if p[3] in func_dir.keys():
       print("Function name already exists.") 
    else:
        new_func = active_scopes.pop()
        new_func.functiontype =  p[1]
        new_func.params = params
        func_dir[p[3]] = new_func

def p_startscope_action(p):
    '''
    startscope_action : 
    '''
    new_function = function_values()
    active_scopes.append(new_function)


def p_recparams(p):
    '''
    recparams : ID COLON type
              | ID COLON type COMMA recparams
    '''
    rule_len = len(p) - 1
    if rule_len == 3:
        p[0] = [variable(p[1],p[3])]
    elif rule_len  == 5:
        p[0] = [variable(p[1],p[3])] + p[5]


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
    recwrite : expression action_recwrite_exp COMMA recwrite 
               | STRING action_recwrite_cte COMMA  recwrite 
               | expression action_recwrite_exp 
               | STRING action_recwrite_cte
    '''
def p_action_recwrite_exp(p):
    '''
    action_recwrite_exp :
    '''
    # We need to validate the ID. Check if it exists.
    result = operand_stack.pop()
    quadruples.append(quadruple("print", None, None, result))

def p_action_recwrite_cte(p):
    '''
    action_recwrite_cte : 
    '''
    quadruples.append(quadruple("print",None, None, p[-1]))

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
    expression : exp RELOP relop_action1 exp relop_action2
               | exp LOGIC logic_action1 exp logic_action2
               | exp
    '''

def p_relop_action1(p):
    '''
    relop_action1 : 
    '''
    operator_stack.append(p[-1])

def p_relop_action2(p):
    '''
    relop_action2 : 
    '''
    print(operand_stack)
    if len(operator_stack) > 0:
        if  operator_stack[-1] in relop_arr:
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operator_stack.pop()
            print(left_type, right_type)

            
            result_type = s_cube.validate_expression(left_type, right_type, operator)
            print(result_type)
            if result_type != "ERROR":
                temp = get_next_avail()
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                print("Type mismatch")


def p_logic_action1(p):
    '''
    logic_action1 : 
    '''
    operator_stack.append(p[-1])

def p_logic_action2(p):
    '''
    logic_action2 : 
    '''
    if len(operator_stack) > 0:
        if  operator_stack[-1] in logic_arr:
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operator_stack.pop()
            result_type = s_cube.validate_expression(left_type, right_type, operator)
            if result_type != "ERROR":
                temp = get_next_avail()
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                print("Type mismatch")

def p_exp(p):
    ''' 
    exp : term exp_action recexp
        | term exp_action 
        '''

def p_exp_action(p):
    '''
    exp_action :
    '''
    if len(operator_stack) > 0:
        if  operator_stack[-1] == "+" or operator_stack[-1] == "-":
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operator_stack.pop()
            result_type = s_cube.validate_expression(left_type, right_type, operator)
            if result_type != "ERROR":
                temp = get_next_avail()
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                print("Type mismatch")


def p_recexp(p):
    ''' 
    recexp : EX add_operator exp 
    '''

def p_term(p):
    ''' 
    term : factor term_action recterm 
         | factor term_action 
    '''

def p_term_action(p):
    '''
    term_action :
    '''
    if len(operator_stack) > 0:
        if  operator_stack[-1] == "*" or operator_stack[-1] == "/":
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operator_stack.pop()
            result_type = s_cube.validate_expression(left_type, right_type, operator)

            if result_type != "ERROR":
                temp = get_next_avail()
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                print("Type mismatch")

def p_recterm(p):
    ''' 
    recterm : TERMS add_operator term
    '''

def p_add_operator(p):
    '''
    add_operator :
    '''    
    operator_stack.append(p[-1])

# add action
def p_factor(p): 
    ''' factor : LEFTPAR expression RIGHTPAR 
               | EX cte 
               | cte 
    '''
    rule_len = len(p) - 1
    if rule_len == 2:
       operand_stack.append(p[2])
       operator_stack.append(p[1])
       types_stack.append(get_type(p[2]))
    elif rule_len == 1:
       operand_stack.append(p[1])
       types_stack.append(get_type(p[1]))
    p[0] = p[1]  

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
    p[0] = p[1]

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