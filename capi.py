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
from util import  get_type_s
from memory import get_next_global, get_next_local, get_next_temporal, get_const_address, get_next_local_list, get_next_global_list
from virtual import init_virtual
import argparse
# Inits the semantic cube
s_cube = semantic_cube()

tokens = (
    'ID','IF','ELSE','EX','TERMS','RELOP','LOGIC','LEFTPAR','RIGHTPAR',
    'LEFTKEY','RIGHTKEY','LEFTBRACKET','RIGHTBRACKET','EQUAL','SEMICOLON',
    'COLON','COMMA','VAR','TINT','TFLOAT','TSTRING','INT','FLOAT','STRING',
    'FOR','FUNC','WHILE','GLOBAL','LIST','TLIST','OBJECT','TOBJECT','DOT','PRINT',
    'RUN','START','RETURN','TRUE','FALSE','TBOOL', 'COMMENT', 'VOID', 'DRAW', 'SIZE','INIT',
    "HEAD","LAST","SET_TITLE","CREATE_TEXT", "UPDATE", "SET_DIMENSION","GET_EVENT","POW","SQRT","QUIT","SET_FILL", 'MAIN',"BAR", "WINDOW_H", "WINDOW_W", "CAPIGAME","FIND","RAND"
)
# This is used to handle reserved words
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
    'init': 'INIT',
    'size':'SIZE',
    'head':'HEAD',
    'find':'FIND',
    'last':'LAST',
    'update' : "UPDATE",
    'set_fill': 'SET_FILL',
    'get_event': 'GET_EVENT',
    'set_title': 'SET_TITLE',
    'create_text': 'CREATE_TEXT',
    'set_dimension': 'SET_DIMENSION',
    'window_h': 'WINDOW_H',
    'window_w': 'WINDOW_W',
    'rand':'RAND',
    'pow':'POW',
    'quit': 'QUIT',
    'sqrt':'SQRT',
    'capigame':'CAPIGAME',
}


# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    type=argparse.FileType("r"),
    help="The capi file used as source",
    required=True,
)
args = parser.parse_args()

fileName = args.file
# Used for generating code
class quadruple():
    def __init__(self, operator, left_operand, right_operand, temp, isptr = False):
        self.id = -1
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.temp = temp
        self.isptr = isptr
    def __str__(self):
        return f'operator: {self.operator}, left_operand: {self.left_operand}, right_operand: {self.right_operand}, temp: {self.temp}, isptr:{self.isptr}\n'
    def __repr__(self):
        return f'operator: {self.operator}, left_operand: {self.left_operand}, right_operand: {self.right_operand}, temp: {self.temp}, isptr:{self.isptr}\n'
# Used for variables
class variable():
    def __init__(self, varid, vartype, address, dim, array_block = None):
        self.id = varid
        self.type = vartype
        self.address = address
        self.dim = dim
        self.array_block = array_block
    def __str__(self):
        return f'Id: {self.id}, Type: {self.type}, Addr: {self.address}, Dim: {self.dim}, ArrayBlock:{self.array_block}'
    def __repr__(self):
        return f'Id: {self.id}, Type: {self.type}, Addr: {self.address}, Dim: {self.dim}, ArrayBlock:{self.array_block}'
# Used for list type variables
class array_block():
    def __init__(self, array_type ,left, right, k):
        self.array_type = array_type
        self.left = left
        self.right = right
        self.k = k
    def __str__(self):
        return f'array_type: {self.array_type}, left: {self.left}, right: {self.right}, k: {self.k}'
    def __repr__(self):
        return f'array_type: {self.array_type}, left: {self.left}, right: {self.right}, k: {self.k}'
# Used for creating function scope
class function_values():
    def __init__(self, functiontype='', params=[], scopevars={}, params_order=[]):
        self.functiontype = functiontype
        self.params = params.copy()
        self.vars = scopevars.copy()
        self.params_order = params_order.copy()
        self.temp_count = 0
        self.cont = -1
    def __str__(self):
        return f'Type: {self.functiontype}, Params: {self.params}, Vars: {self.vars}, Params_Order: {self.params_order}, CONT: {self.cont}, TEMP_COUNT: {self.temp_count}\n'
    def __repr__(self):
        return f'Type: {self.functiontype}, Params: {self.params}, Vars: {self.vars}, Params_Order: {self.params_order}, CONT: {self.cont}, TEMP_COUNT: {self.temp_count}\n'
# Gets the type of the id
def get_typeof_id(inc_id):
    current_active_scopes = active_scopes.copy()
    current_type = ""
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if inc_id in current_vars:
            current_type = current_vars[inc_id].type
            break
        current_active_scopes.pop()
    
    if(len(current_active_scopes) <= 0):
        raise Exception("Variable does not exist")
    else:
        operand_stack.append(inc_id)
        types_stack.append(current_type)
    return current_type
# Gets the type of id for both vars and params
def get_typeof_id_vp(inc_id):
    current_active_scopes = active_scopes.copy()
    current_type = ""
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        current_params = current_active_scopes[-1].params
        for param in current_params:
            if inc_id == param.id:
                current_type = param.type
                break
        if inc_id in current_vars:
            current_type = current_vars[inc_id].type
            break
        current_active_scopes.pop()
    if(len(current_active_scopes) <= 0 and current_type == ""):
        raise Exception("Variable does not exist.")
   
    return current_type


def get_next_avail(tp, convert = True):
    global temporals
    temporals +=1
    if convert:
        return get_next_temporal(get_type_s(tp))
    return get_next_temporal(tp)

quadruples = [] # Quadruple List
current_callId = '' # This is the id of the current function call
current_returnAddress = '' # This is the current return Address when handling returns in functions
is_assign_for = False # We use this when handling assignation of variables inside forloop
current_functionId = '' # This is the id of the current function. It is used when declaring functions
operator_stack = deque() # Operator Stack
operand_stack = deque() # Operand Stack
types_stack = deque() # Types Stack
go_to_stack = deque() # Jump Stack
dimension_stack = deque() #Used to store the current dimension of the array
params_stack = deque() # We use this to handle params
expression_counter = 0 # We use this to count the expressions
temporals = 0 # This is used to count the temporals in a context

func_dir = {} # Function Directory
active_scopes = deque() # Scope stacks
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
t_BAR = r'\|'

relop_arr = ['<=',">=",">","<","!=","=="]
logic_arr = ["||","&&"]

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t 

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"[a-zA-Z_ ][a-zA-Z0-9_ ]*\"'
    return t

def t_TRUE(t):
    r'(true)'
    t.value = 1
    return t

def t_FALSE(t):
    r'(false)'
    t.value = 0
    return t

def t_COMMENT(t):
    r'\@.*'
    pass
    # No return value. Token discarded

# Ignored characters
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
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lex = lex.lex()


# Program
def p_capi(p):
    ''' 
    capi : capi_action1 global recfunc MAIN COLON LEFTKEY start capi_action2 run RIGHTKEY SEMICOLON
         | capi_action1 recfunc MAIN COLON LEFTKEY start capi_action2 run RIGHTKEY SEMICOLON
         | capi_action1 global MAIN COLON LEFTKEY start capi_action2 run RIGHTKEY SEMICOLON
         | capi_action1 MAIN COLON LEFTKEY start capi_action2 run RIGHTKEY SEMICOLON
    '''
def p_capi_action1(p):
    '''
    capi_action1 :
    '''
    # This goto is created to be used later in the start function. This is used so that at the start of the
    # program it jumps to the start function.
    quadruples.append(quadruple("GOTO",None,None,None))

def p_capi_action2(p):
    '''
    capi_action2 :
    '''
    quadruples[0] = quadruple("GOTO",None,None,func_dir['start'].cont - 1)

def p_global(p):
    '''
    global : GLOBAL COLON LEFTKEY vars RIGHTKEY SEMICOLON
           | GLOBAL COLON LEFTKEY RIGHTKEY SEMICOLON
    '''
    globalscope = active_scopes.pop()
    func_dir['global'] = globalscope
    active_scopes.append(globalscope)

    
def p_start(p):
    '''
    start : VOID FUNC start_action1 START startscope_action LEFTPAR RIGHTPAR main_cont block 
    '''
    # We add the start function to the func dir
    global temporals
    new_func = active_scopes.pop()
    new_func.temp_count = temporals
    temporals = 0
    new_func.functiontype =  'void'
    new_func.params = []
    new_func.params_order = []
    
    func_dir[p[4]] = new_func
    quadruples.append(quadruple("ENDFUNC", None,None, None))


def p_start_action1(p):
    '''
    start_action1 :
    '''
    quadruples.append(quadruple("ERA","start" ,None, None))
    quadruples.append(quadruple("GOSUB","start",None,None))

def p_run(p):
    '''
    run : VOID FUNC run_action1 RUN startscope_action LEFTPAR RIGHTPAR main_cont block 
    '''
    global temporals
    new_func = active_scopes.pop()
    new_func.temp_count = temporals
    temporals = 0
    new_func.functiontype =  'void'
    new_func.params = []
    new_func.params_order = []
    
    func_dir[p[4]] = new_func
    quadruples.append(quadruple("GOTO", None, None, go_to_stack.pop()))
    quadruples.append(quadruple("ENDFUNC", None,None, None))

def p_run_action1(p):
    '''
    run_action1 :
    '''
    quadruples.append(quadruple("ERA", "run",None, None))
    quadruples.append(quadruple("GOSUB","run",None,None))
    go_to_stack.append(len(quadruples))

def p_main_cont(p):
    '''
    main_cont :
    '''
    active_scopes[-1].cont = len(quadruples) - 1

def p_vars(p): 
    ''' 
    vars : VAR recids COLON type SEMICOLON vars
            | VAR recids COLON type SEMICOLON
    '''
    global dimension_stack
    rule_len = len(p) - 1
    current_function = active_scopes.pop()
    address = 0
    current_list_addr = 0 # We use this to handle multiple declarations with same dimension
    addr_popped = False  # We use this to handle multiple declarations with same dimension
    # We use a for in here so that we can handle multiple declarations
    for l in p[2]:
        if p[4][0] == 'list':
            if not addr_popped:
                current_list_addr = dimension_stack.pop()
                addr_popped = True
        if(current_function.functiontype == 'global'):
            # We create global addresses
            if p[4][0] == 'list':
                address = get_next_global_list(p[4][1], current_list_addr)
            else:
                address = get_next_global(p[4])
        else:
            if p[4][0] == 'list':
                address = get_next_local_list(p[4][1], current_list_addr)
            else:
                address = get_next_local(p[4])
        if p[4][0] == 'list':
            current_function.vars[l] = variable(l,p[4][0], address,1, array_block(p[4][1],get_const_address(0,'i'),current_list_addr,get_const_address(0,'i')))
        else:   
            current_function.vars[l] = variable(l,p[4], address,get_const_address(0,'i'))
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
        p[0] = [p[1]] + p[3]

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
              | specialfunction SEMICOLON
    '''
    # In here we are sending the first instruction of our grammar
    p[0] = p[1]

def p_specialfunction(p):
    '''
    specialfunction : draw
                    | init
                    | size
                    | head
                    | find
                    | last
                    | set_fill
                    | set_title
                    | get_event
                    | update
                    | window_h
                    | window_w
                    | set_dimension
                    | create_text
                    | rand
                    | pow
                    | sqrt
                    | quit
    '''
    p[0] = p[1]

def p_quit(p):
    '''
    quit : QUIT LEFTPAR RIGHTPAR
    '''
    quadruples.append(quadruple('QUIT', None, None, None))

def p_pow(p):
    '''
    pow : POW pow_action1 LEFTPAR expression COMMA expression RIGHTPAR
    '''
    pot = operand_stack.pop()
    types_stack.pop()
    num = operand_stack.pop()
    t = types_stack.pop()
    temp = get_next_avail('f', False)
    quadruples.append(quadruple('POW', num, pot, temp))
    operator_stack.pop()
    p[0] = (temp, 'f')

def p_pow_action1(p):
    '''
    pow_action1 :
    '''
    operator_stack.append("|WALL|")

def p_sqrt(p):
    '''
    sqrt : SQRT sqrt_action1 LEFTPAR expression RIGHTPAR
    '''
    num = operand_stack.pop()
    t = types_stack.pop()
    temp = get_next_avail(t, False)
    quadruples.append(quadruple('SQRT', num, None, temp))
    operator_stack.pop()
    p[0] = (temp, t)

def p_sqrt_action1(p):
    '''
    sqrt_action1 :
    '''
    operator_stack.append("|WALL|")



def p_draw(p):
    '''
    draw : CAPIGAME DOT DRAW LEFTPAR expression COMMA expression COMMA expression COMMA expression COMMA expression RIGHTPAR
    '''
    height = operand_stack.pop()
    types_stack.pop()
    width = operand_stack.pop()
    types_stack.pop()
    y = operand_stack.pop()
    types_stack.pop()
    x = operand_stack.pop()
    types_stack.pop()
    color = operand_stack.pop()
    types_stack.pop()
    temp = get_next_avail('o', False)
    quadruples.append(quadruple('DRAW', color, (x,y,width,height), temp))
    p[0] = (temp, 'o')

def p_init(p):
    '''
    init : CAPIGAME DOT INIT LEFTPAR RIGHTPAR
    '''
    quadruples.append(quadruple('INIT', None, None, None))

def p_size(p):
    '''
    size : ID DOT SIZE LEFTPAR RIGHTPAR
    '''
    var_id = p[1]
    id_valid = False
    size = 0
    current_active_scopes = active_scopes.copy()
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if var_id in current_vars:
            if current_vars[var_id].type == 'list':
                is_valid = True
                size = current_vars[var_id].array_block.right
            else:
                is_valid = False
            break
        current_active_scopes.pop()
 
    if(len(current_active_scopes) <= 0 ):
        raise Exception("Variable does not exist")
    if not is_valid:
        raise Exception("Size function does not exist for this type of variable.")

    temp = get_next_avail('i', False)
    quadruples.append(quadruple('SIZE', size, None, temp))
    p[0] = (temp, 'i')

def p_head(p):
    '''
    head : ID DOT HEAD LEFTPAR RIGHTPAR
    '''
    var_id = p[1]
    id_valid = False
    address = 0
    element_type = ''
    current_active_scopes = active_scopes.copy()
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if var_id in current_vars:
            if current_vars[var_id].type == 'list':
                is_valid = True
                address = current_vars[var_id].address
                element_type = current_vars[var_id].array_block.array_type
            else:
                is_valid = False
            break
        current_active_scopes.pop()
    if(len(current_active_scopes) <= 0 ):
        raise Exception("Variable does not exist")
    if not is_valid:
        raise Exception("Size function does not exist for this type of variable.")

    temp = get_next_avail(element_type, False)
    quadruples.append(quadruple('HEAD', address, None, temp))
    p[0] = (temp, element_type)

# Height of the window
def p_window_h(p):
    '''
    window_h : CAPIGAME DOT WINDOW_H LEFTPAR RIGHTPAR
    '''
    temp = get_next_avail('i', False)
    quadruples.append(quadruple('WINDOW_H', None, None, temp))
    p[0] = (temp, 'i')

# Width of the window
def p_window_w(p):
    '''
    window_w : CAPIGAME DOT WINDOW_W LEFTPAR RIGHTPAR
    '''
    temp = get_next_avail('i', False)
    quadruples.append(quadruple('WINDOW_W', None, None, temp))
    p[0] = (temp, 'i')
# Random number
def p_rand(p):
    '''
    rand : CAPIGAME DOT RAND LEFTPAR expression COMMA expression RIGHTPAR
    '''
    sup_num = operand_stack.pop()
    types_stack.pop()
    inf_num = operand_stack.pop()
    types_stack.pop()

    temp = get_next_avail('i', False)
    quadruples.append(quadruple('RAND', inf_num, sup_num, temp))
    p[0] = (temp, 'i')
# Find an element in an array
def p_find(p):
    '''
    find : ID DOT FIND LEFTPAR expression RIGHTPAR
    '''
    var_id = p[1]
    id_valid = False
    find_value = operand_stack.pop()
    types_stack.pop()
    address = 0
    element_type = ''
    right = 0
    current_active_scopes = active_scopes.copy()
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if var_id in current_vars:
            if current_vars[var_id].type == 'list':
                is_valid = True
                address = current_vars[var_id].address
                right = current_vars[var_id].array_block.right
                element_type = current_vars[var_id].array_block.array_type
            else:
                is_valid = False
            break
        current_active_scopes.pop()
    if(len(current_active_scopes) <= 0 ):
        raise Exception("Variable does not exist")
    if not is_valid:
        raise Exception("Find function does not exist for this type of variable.")

    temp = get_next_avail('b', False)
    quadruples.append(quadruple('FIND', (address, right), find_value, temp))
    p[0] = (temp, 'b')
# Gets the last element of an array
def p_last(p):
    '''
    last : ID DOT LAST LEFTPAR RIGHTPAR
    '''
    var_id = p[1]
    id_valid = False
    address = 0
    element_type = ''
    right = 0
    current_active_scopes = active_scopes.copy()
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if var_id in current_vars:
            if current_vars[var_id].type == 'list':
                is_valid = True
                address = current_vars[var_id].address
                right = current_vars[var_id].array_block.right
                element_type = current_vars[var_id].array_block.array_type
            else:
                is_valid = False
            break
        current_active_scopes.pop()
    if(len(current_active_scopes) <= 0 ):
        raise Exception("Variable does not exist")
    if not is_valid:
        raise Exception("Last function does not exist for this type of variable.")

    temp = get_next_avail(element_type, False)
    quadruples.append(quadruple('LAST', address, right, temp))
    p[0] = (temp, element_type)
    
# Sets the window title
def p_set_title(p):
    '''
    set_title : CAPIGAME DOT SET_TITLE LEFTPAR expression RIGHTPAR
    '''
    title = operand_stack.pop()
    title_type = types_stack.pop()
    # Quadruple used to send the title to the VM
    if title_type == 's':
        quadruples.append(quadruple('SET_TITLE', title, None, None))
    else:
        raise Exception("The title expression must be a string.")
# Sets the color of the window
def p_set_fill(p):
    '''
    set_fill : CAPIGAME DOT SET_FILL LEFTPAR expression COMMA expression COMMA expression RIGHTPAR
    '''  
    b = operand_stack.pop()
    g = operand_stack.pop()
    r = operand_stack.pop()
    types_stack.pop()
    types_stack.pop()
    types_stack.pop()
    quadruples.append(quadruple('SET_FILL', r, g, b))
# Sets the dimension of the window    
def p_set_dimension(p):
    '''
    set_dimension : CAPIGAME DOT SET_DIMENSION LEFTPAR expression COMMA expression RIGHTPAR
    '''
    x = operand_stack.pop()
    y = operand_stack.pop()
    types_stack.pop()
    types_stack.pop()
    # Quadruple used to send the dimension to the VM
    quadruples.append(quadruple('SET_DIM', x, y, None))
# Updates the objects inside the run module.
def p_update(p):
    '''
    update : CAPIGAME DOT UPDATE LEFTPAR RIGHTPAR
    '''
    quadruples.append(quadruple('UPDATE', None, None, None))
# Gets the pygame events.
def p_get_event(p):
    '''
    get_event : CAPIGAME DOT GET_EVENT LEFTPAR RIGHTPAR
    '''
    temp = get_next_avail('s', False)
    quadruples.append(quadruple('GET_EVENT', None, None, temp))
    p[0] = (temp, 's')

# Creates a text object
def p_create_text(p):
    '''
    create_text : CREATE_TEXT LEFTPAR expression COMMA expression COMMA expression COMMA expression RIGHTPAR
    '''
    y = operand_stack.pop()
    types_stack.pop()
    x = operand_stack.pop()
    types_stack.pop()
    color = operand_stack.pop()
    types_stack.pop()
    text = operand_stack.pop()
    types_stack.pop()

    temp = get_next_avail('o', False)
    quadruples.append(quadruple('CREATE_TEXT', text,(color,x,y), temp))
    p[0] = (temp, 'o')
    
def p_assign(p):
    '''
    assign : ID assign_action1 EQUAL assign_action2 expression 
           | assign_list EQUAL assign_action2 expression
    '''
    # we need to do the same for var i :int = 5;
    global is_assign_for
    # We use this to ignore the wall and just pop it
    if operator_stack[-1] == '|WALL|':
        operator_stack.pop()
    
    result = operand_stack.pop()
    type_result = types_stack.pop()
    quad_list = []
    if len(operand_stack) > 0:
        left_operand = operand_stack.pop()
        left_operand_type = types_stack.pop()
        operator = operator_stack.pop()
        # We use this to distinguish list assign from the other types
        if type(left_operand) is tuple:
            expression_type = s_cube.validate_expression(type_result, left_operand_type, operator)
            if expression_type != "ERROR":
                address = ""
                var_type = ""
                current_active_scopes = active_scopes.copy()
                while len(current_active_scopes) != 0:
                    current_vars = current_active_scopes[-1].vars
                    if left_operand[0] in current_vars:
                        address = current_vars[left_operand[0]].address
                        var_type = current_vars[left_operand[0]].type
                        break
                    current_active_scopes.pop()
                    
                if(len(current_active_scopes) <= 0):
                    raise Exception("Variable does not exist")
                else:
                    quadruples.append(quadruple(operator, result, None, left_operand[1], True))
            else:
                raise Exception("Type mismatch at assignation")
        else:
            expression_type = s_cube.validate_expression(type_result, left_operand_type, operator)
            if expression_type != "ERROR":
                address = ""
                var_type = ""
                current_active_scopes = active_scopes.copy()
                while len(current_active_scopes) != 0:
                    current_vars = current_active_scopes[-1].vars
                    if left_operand in current_vars:
                        address = current_vars[left_operand].address
                        var_type = current_vars[left_operand].type
                        break
                    current_active_scopes.pop()
                    
                if(len(current_active_scopes) <= 0):
                    raise Exception("Variable does not exist")
                else:
                    quad_list.append(quadruple(operator, result, None, address))
                    if not is_assign_for:
                        quadruples.append(quadruple(operator, result, None, address))
            else:
                raise Exception("Type mismatch at assignation")
            if is_assign_for:
                p[0] = quad_list
            is_assign_for = False
            quad_list = []

def p_assign_action1(p):
    '''
    assign_action1 : 
    '''
    current_id = p[-1] # Get current ID
    get_typeof_id(current_id)



def p_assign_action2(p):
    '''
    assign_action2 : 
    '''
    operator_stack.append(p[-1])


def p_condition(p):
    ''' condition : IF LEFTPAR expression condition_action1 RIGHTPAR  block condition_action2
                  | IF LEFTPAR expression condition_action1 RIGHTPAR  block condition_action3 ELSE  block condition_action2
     '''
     
def p_condition_action1(p):
    '''
    condition_action1 :
    '''
    exp_type = types_stack.pop()
    if exp_type != "b":
        raise Exception("Type mismatch.")
    else:
        result = operand_stack.pop()
        # We generate our Goto_F for the if statement
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
    # We generate the GOTO Quadruple when we have an else in our if
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
    for : FOR startscope_action LEFTPAR  assign  SEMICOLON for_action1 expression for_action2 SEMICOLON assign SEMICOLON RIGHTPAR block for_action3
    '''
    new_func = active_scopes.pop() # Get the last function created
    new_func.functiontype =  ""  # We clear out the name of the function
    new_func.params = []

def p_for_action1(p):
    '''
    for_action1 : 
    '''
    global is_assign_for
    is_assign_for = True
    go_to_stack.append(len(quadruples))

def p_for_action2(p):
    '''
    for_action2 : 
    '''
    cond = operand_stack.pop()
    cond_type = types_stack.pop()

    if cond_type != "b":
        raise Exception("Type mismatch.")
    else:
        # We use this GOTO_F to handle our for loop if the condition is false
        quadruples.append(quadruple("GOTO_F", cond,None,None))
        go_to_stack.append(len(quadruples)-1)
        
def p_for_action3(p):
    '''
    for_action3 : 
    '''
    falso = go_to_stack.pop() 
    ref = go_to_stack.pop()
    quad_list = p[-4]
    for quad in quad_list:
        quadruples.append(quad)
    # We generate this to return to the expresion and re evaluate it
    quadruples.append(quadruple("GOTO", None, None, ref))
    quadruples[falso] = quadruple(quadruples[falso].operator, quadruples[falso].left_operand,None, len(quadruples))
    
    
def p_while(p):
    '''
    while : WHILE startscope_action while_action1 LEFTPAR expression while_action2 RIGHTPAR block while_action3
    '''
    new_func = active_scopes.pop() # Get the last function created
    new_func.functiontype =  ""  # Assign empty string to the function type
    new_func.params = []


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
        raise Exception("Type mismatch.")
    else:
        # We use this quadruple to handle when the while expression is false
        quadruples.append(quadruple("GOTO_F", cond,None,None))
        go_to_stack.append(len(quadruples)-1)

def p_while_action3(p):
    '''
    while_action3 :
    '''
    falso = go_to_stack.pop() 
    ref = go_to_stack.pop()
    # We generate this to return to the expresion and re evaluate it
    quadruples.append(quadruple("GOTO", None, None, ref))
    quadruples[falso] = quadruple(quadruples[falso].operator, quadruples[falso].left_operand,None, len(quadruples))

def p_function(p):
    '''
    function : type FUNC ID startscope_action LEFTPAR recparams function_action1 RIGHTPAR function_action2 function_action3 block
             | type FUNC ID startscope_action LEFTPAR RIGHTPAR function_action3 block
             | VOID FUNC ID startscope_action LEFTPAR recparams function_action1 RIGHTPAR function_action2 function_action3 block
             | VOID FUNC ID startscope_action LEFTPAR RIGHTPAR function_action3 block
    '''
    global temporals, current_functionId,current_returnAddress
    new_func = active_scopes.pop()
    new_func.temp_count = temporals
    # We generate this quadruple to hanlde when the function terminates
    quadruples.append(quadruple("ENDFUNC",None,None,None))
    temporals = 0
    func_dir[p[3]] = new_func # We add the function to the function directory
    if p[1] != "void":
        # TODO We need to handle this error
        if current_functionId in func_dir['global'].vars:
            add = func_dir['global'].vars[current_functionId].address
            for quad in quadruples:
                if quad.operator != 'ERA' and quad.operator != 'GOSUB':
                    if quad.left_operand == current_functionId:
                        quad.left_operand = add
                    if quad.right_operand == current_functionId:
                        quad.right_operand = add
                    if quad.temp == current_functionId:
                        quad.temp = add
        else:
            raise Exception("Return missing in function:", current_functionId)
    current_functionId = ""
    current_returnAddress = ""
    

# We use this to handle scopes between, functions, while, for and if statements
def p_startscope_action(p):
    '''
    startscope_action : 
    '''
    global current_functionId
    if p[-1] in func_dir.keys():
        raise Exception("Function name already exists.")
    
    else:
        if p[-1] != 'for' and p[-1] != 'while' and p[-1] != 'if':
            current_functionId = p[-1]
            new_function = function_values()
            new_function.functiontype = p[-3]
            active_scopes.append(new_function)
        else:
            new_function = function_values()
            new_function.functiontype = p[-3]
            active_scopes.append(new_function)

def p_function_action1(p):
    '''
    function_action1 :
    '''
    active_scopes[-1].params = p[-1]
    
def p_function_action2(p):
    '''
    function_action2 :
    '''
    params_order = []
    current_params = active_scopes[-1].params
    for current_p in current_params:
         params_order.append(current_p.type)
    
    active_scopes[-1].params_order = params_order

def p_function_action3(p):
    '''
    function_action3 :
    '''
    global current_functionId
    func_dir[current_functionId] = active_scopes[-1]
    active_scopes[-1].cont = len(quadruples) - 1

# We use this to handle multiple or single parameters in functions
def p_recparams(p):
    '''
    recparams : ID COLON type
              | ID COLON type COMMA recparams
    '''

    rule_len = len(p) - 1
    address = get_next_local(p[3])
    if rule_len == 3:
        p[0] = [(variable(p[1],p[3],address,get_const_address(0,'i')))]
    elif rule_len  == 5:
        p[0] = [(variable(p[1],p[3],address,get_const_address(0,'i')))] + p[5]
    

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
    result = operand_stack.pop()
    types_stack.pop()
    # We use this quadruple to handle prints in our lang
    quadruples.append(quadruple("print", None, None, result))

def p_action_recwrite_cte(p):
    '''
    action_recwrite_cte : 
    '''
    address = get_const_address(p[-1], 's')
    quadruples.append(quadruple("print",None, None, address))

def p_return(p):
    '''
     return : RETURN expression
    '''
    global current_functionId,current_returnAddress
    #print(active_scopes)
    func_type = active_scopes[-1].functiontype
    operand_type = types_stack.pop()
    operand_value = operand_stack.pop()


    if current_returnAddress == "":
        return_address = get_next_global(operand_type)
        current_returnAddress = return_address
        func_dir['global'].vars[current_functionId] = variable(current_functionId, operand_type, current_returnAddress,0)

    if func_type != "void":
        if func_type == operand_type:
            # When the function returns a value then we assign the value to the return address.
            quadruples.append(quadruple('=',operand_value,None,current_returnAddress))
            # We terminate the function using endfunc
            quadruples.append(quadruple('ENDFUNC', None, None, None))
        else:
            raise Exception("Type mismatch")
    else:
        raise Exception("Cannot return value in void function.")


def p_functioncall(p):
    '''
    functioncall : ID function_call_action1 LEFTPAR function_call_action2 recfuncexp RIGHTPAR 
                 | ID function_call_action1 LEFTPAR  function_call_action2 RIGHTPAR 
    '''
    global current_callId,func_dir
    rule_len = len(p)- 1
    # This is used to validate function calls without params
    if rule_len == 5:
        if current_callId in func_dir:
            params = func_dir[current_callId].params_order
        else:
            params = active_scopes[-1].params_order 
        if(len(params) > 0):
            raise Exception("Params mismatch.")
    # We generate a GOSUB so that will be used to jump to the function quadruple counter
    quadruples.append(quadruple("GOSUB", current_callId, None, None))
    if current_callId in func_dir:
        func_type = func_dir[current_callId].functiontype 
        if func_type != 'void':
            temp = get_next_avail(func_type, False)
            current_returnAddress = func_dir["global"].vars[current_callId].address
            # For each function called we will create a temp and assign it to the return address.
            quadruples.append(quadruple('=',current_returnAddress,None,temp))
    if current_callId in func_dir["global"].vars:
        operand = func_dir["global"].vars[current_callId].address
        t = func_dir["global"].vars[current_callId].type
    elif current_callId == current_functionId:
        operand = current_callId
        t = active_scopes[-1].functiontype
    elif current_callId in func_dir.keys():
        operand = ''
        t = ''
    else: 
        raise Exception('Function does not exists.')

    if func_type != 'void':
        p[0] = (temp,func_type)
    else: 
        pass
    
    current_callId = ''

def p_function_call_action1(p):
    '''
    function_call_action1 : 
    '''
    id = p[-1]
    if id not in func_dir.keys() and id != current_functionId:
       raise Exception("Function does not exist.")
    else:
        global current_callId
        current_callId = id
       

def p_function_call_action2(p):
    '''
    function_call_action2 : 
    '''
    operator_stack.append("|WALL|")
    quadruples.append(quadruple("ERA",p[-3],None,None))

    
  
def p_recfuncexp(p):
    '''
    recfuncexp : expression exp_action1 COMMA recfuncexp
               | expression exp_action1 recfunc_action1
    '''
    rule_len = len(p) -1
    if rule_len == 2:
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_exp_action1(p):
    '''
    exp_action1 :
    '''
    global expression_counter
    expression_counter  = expression_counter + 1

def p_recfunc_action1(p):
    '''
    recfunc_action1 :
    '''
    global current_callId,expression_counter, params_stack
    params_stack.append(expression_counter)
    
    if current_callId in func_dir:
        param_order = func_dir[current_callId].params_order
    else:
        param_order = active_scopes[-1].params_order

    params_order = []

    copy_types = types_stack.copy()
    copy_operands = operand_stack.copy()
    k = len(param_order) - 1
    for ty in copy_types:
        copy_operands.pop()
        params_order.append(ty)

    if operator_stack:
        if operator_stack[-1] == '=':
            params_order.pop()
    
    counter = 0
    q_operand_stack = operand_stack.copy()
    if len(param_order) != params_stack[-1]:
        raise Exception("Params Mismatch.")
    while counter <= k:
        if param_order[counter] == params_order[counter]:
            quadruples.append(quadruple("PARAM", q_operand_stack.pop(), None, "Param " + str(counter + 1)))
            operand_stack.pop()
            types_stack.pop()
        else:
            raise Exception("Param type mismatch")
        counter+=1
   # verify that all parameters where processed 
    if counter - 1 == k:
        #print("All parameters where processed")
        params_stack.pop()
        expression_counter = 0
        operator_stack.pop()
    p[0] = params_order
    
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
    if len(operator_stack) > 0:
        if  operator_stack[-1] in relop_arr:
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operator_stack.pop()
            result_type = s_cube.validate_expression(left_type, right_type, operator)
            if result_type != "ERROR":
                temp = get_next_avail(result_type)
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                raise Exception("Type mismatch.")


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
                temp = get_next_avail(result_type)
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                raise Exception("Type mismatch.")

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
                temp = get_next_avail(result_type)
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                raise Exception("Type mismatch.")


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
                temp = get_next_avail(result_type)
                quadruples.append(quadruple(operator, left_operand, right_operand, temp))
                operand_stack.append(temp)
                real_type = get_type_s(result_type)
                types_stack.append(real_type)
                # return to avail if operand were a temp
            else:
                raise Exception("Type mismatch")

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
    ''' factor : factor_action1 LEFTPAR expression RIGHTPAR factor_action2 
               | EX cte 
               | cte 
    '''
    rule_len = len(p) - 1
    if rule_len == 2:
       operand_stack.append(p[2][0])
       operator_stack.append(p[1])
       types_stack.append(p[2][1])
    elif rule_len == 1:
       operand_stack.append(p[1][0])
       types_stack.append(p[1][1])
    p[0] = p[1]  

def p_factor_action1(p):
    '''
    factor_action1 :
    '''
    # We use this so that the expression respects the order of operations.
    operator_stack.append("|WALL|")
def p_factor_action2(p):
    '''
    factor_action2 :
    '''
    operator_stack.pop()

def p_type(p):
    '''
    type : primitivetype
        | TLIST BAR primitivetype BAR LEFTBRACKET cte RIGHTBRACKET action_list1
    '''
    rule_len = len(p) - 1
    if rule_len == 1:
        p[0] = p[1]
    else:
        p[0] = (p[1],p[3])
def p_action_list1(p):
    '''
    action_list1 :
    '''
    global dimension_stack
    size = p[-2]
    if size[1] != 'i':
        raise Exception("Type mismatch in list.")
    dimension_stack.append(size[0])
def p_primitivetype(p):
    '''
    primitivetype : TINT
                  | TFLOAT
                  | TSTRING
                  | TBOOL
    '''
    p[0] = p[1][0].lower()


def p_assign_list(p):
    '''
    assign_list : ID list_action1 LEFTBRACKET expression  list_action_3 RIGHTBRACKET 
    '''
    aux1 = operand_stack.pop()
    aux1_type = types_stack.pop()
    list_obj = get_list_obj(p[1])
    temp = get_next_avail(aux1_type, False)
    quadruples.append(quadruple("+", aux1,list_obj.address,temp, False))
    operand_stack.append((operand_stack.pop(),temp)) # This is used when assigning elements to a list
    p[0] = (temp,aux1_type)
        
def p_listaccess(p):
    '''
    listaccess : ID list_action1 LEFTBRACKET expression  list_action_3 RIGHTBRACKET 
    '''
    aux1 = operand_stack.pop()
    aux1_type = types_stack.pop()
    list_obj = get_list_obj(p[1])
    temp = get_next_avail(aux1_type, False)
    quadruples.append(quadruple("+", aux1,list_obj.address,temp, True))
    operand_stack.pop() 
    types_stack.pop()
    operator_stack.pop() # pop our |WALL|
    p[0] = (temp,aux1_type)
def p_list_action1(p):
    '''
    list_action1 :
    '''
    list_obj = get_list_obj(p[-1])
    operand_stack.append(list_obj.id)
    types_stack.append(list_obj.array_block.array_type)
    operator_stack.append("|WALL|") # We use this so that we can handle operations between lists

def p_list_action_3(p):
    '''
    list_action_3 :
    '''
    list_obj = get_list_obj(p[-4])
    # We create this quadruple to verify the dimensions of the array
    quadruples.append(quadruple("VERIFY", operand_stack[-1],list_obj.array_block.left, list_obj.array_block.right))

# This utility function is used to get the list object so that we can manipulate it.
def get_list_obj(id):
    current_active_scopes = active_scopes.copy()
    list_obj = None
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        if id in current_vars:
            list_obj = current_vars[id]
            break
        current_active_scopes.pop()
    if list_obj == None:
        raise Exception("List does not exist")
    return list_obj

def p_cte(p):
    '''
    cte :    
        | id
        | int
        | float
        | bool
        | string
        | functioncall
        | listaccess
        | specialfunction
    '''
    p[0] = p[1]

def p_id(p):
    '''
    id : ID
    '''
    current_active_scopes = active_scopes.copy()
    id_address = ""
    while len(current_active_scopes) != 0:
        current_vars = current_active_scopes[-1].vars
        current_params = current_active_scopes[-1].params
        for param in current_params:
            if p[1] == param.id:
                id_address = param.address
                break
        if p[1] in current_vars:
            id_address = current_vars[p[1]].address
            break
        if id_address == "":
            current_active_scopes.pop()
        else:
            break
    p[0] = (id_address, get_typeof_id_vp(p[1]))

def p_string(p):
    '''
    string : STRING
    '''
    addr = get_const_address(p[1],'s')
    p[0] = (addr, 's')

def p_int(p):
    '''
    int : INT
    '''
    addr = get_const_address(p[1],'i')
    p[0] = (addr, 'i')
    
def p_float(p):
    '''
    float : FLOAT
    '''
    addr = get_const_address(p[1],'f')
    p[0] = (addr, 'f')

def p_bool(p):
    '''
    bool : TRUE 
         | FALSE
    '''
    addr = get_const_address(p[1],'b')
    p[0] = (addr, 'b')

def p_error(p):
    print("ERROR {}".format(p))
    print(f"Syntax error at {p.value!r}")
    exit()
    
import ply.yacc as yacc
yacc.yacc()


f = open(fileName.name)
s = f.read()
f.close()

yacc.parse(s)

print('Code compiled sucessfully.')
init_virtual(quadruples, func_dir)