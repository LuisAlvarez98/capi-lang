from collections import deque #Para el stack de scopes

global_int = 0
global_float = 5000
global_string = 10000
global_bool  = 15000
global_object = 20000

local_int = 25000
local_float =  30000
local_string = 35000
local_bool = 40000
local_object = 45000

temporal_int = 50000
temporal_float = 55000
temporal_string = 60000
temporal_bool = 65000
temporal_object = 70000

constant_int = 75000
constant_float = 80000
constant_string = 85000
constant_bool = 90000
constant_object = 95000

GLOBAL_START = 0
LOCAL_START = 25000
TEMPORAL_START = 50000
CONSTANT_START = 75000



class memory():
    def __init__(self, value='', address='', array_block=None):
        self.value = value
        self.address= address
        self.array_block = array_block
    def __str__(self):
        return f'Value: {self.value}, Addr: {self.address}\n'
    def __repr__(self):
        return f'Value: {self.value}, Addr: {self.address}\n'


call_stack = deque()

class func_memory():
    def __init__(self, function_name='', cont=-1, memory_list={}, params={}):
        self.function_name = function_name
        self.cont= cont
        self.prev = 0
        self.memory_list = memory_list.copy()
        self.params = params.copy()
    def __str__(self):
        return f'Function Name: {self.function_name}, Cont: {self.cont}, Memory List: {self.memory_list}, Params: {self.params}, Prev: {self.prev}\n'
    def __repr__(self):
        return f'Function Name: {self.function_name}, Cont: {self.cont}, Memory List: {self.memory_list}, Params: {self.params}, Prev: {self.prev}\n'

function_list = {}
memory_table = {}
constant_table= {}


def init_memory(func_dir):
    global call_stack, param_counter
    for func_key in func_dir:
        func = func_dir[func_key]
        memory_list = {}
        params = {}
        current_vars = func.vars
        current_params = func.params
        param_counter = len(current_params) - 1
        for v in current_vars.values():
            if v.type == 'list':
                addr = v.address #we store the base address
                memory_list[v.address] = memory(v.address,v.address, v.array_block)
                for i in range(0,memory_table[v.array_block.right].value):
                    # we generate the memory of the array with the default value
                    addr = addr + 1
                    memory_list[addr] = memory(get_default_value(v.array_block.array_type), addr)
            else:
                memory_list[v.address] = memory(get_default_value(v.type),v.address)
        for p in current_params:
            # TODO arrays in params
            params[param_counter] = memory(get_default_value(p.type),p.address)
            param_counter-=1
        function_list[func_key] = func_memory(func_key,func.cont, memory_list,params)     
        if func_key == "global":
            call_stack.append(func_memory(func_key,func.cont, memory_list,params))
def create_func_memory(id):
    temp = function_list[id]
    temp_mem = temp.memory_list.copy()
    temp_params = temp.params.copy()
    copy_mem = {}
    copy_params = {}
    param_counter = len(temp_params)-1
    for v in temp_mem.values():
        copy_mem[v.address] = memory(v.value,v.address)
    for p in temp_params.values():
        copy_params[param_counter] = memory(p.value,p.address)
        param_counter-=1

    fm = func_memory(temp.function_name, temp.cont,temp_mem ,copy_params )
    return fm

def get_default_value(t):
    if t == 'i':
        return 0
    elif t == 's':
        return ""
    elif t == 'f':
        return 0
    elif t == 'b':
        return False
    elif t == 'o':
        return None

def get_const_address(value, type):
    if value in constant_table.keys():
        return constant_table[value].address
    address = get_next_constant(type)
    new_value = memory(value, address)
    constant_table[value] =  new_value
    memory_table[address] = new_value
    return address

def get_next_global(t):
    if(t == "i"):
        global global_int
        global_int = global_int + 1
        return global_int
    elif (t == "f"):
        global global_float
        global_float = global_float + 1
        return global_float 
    elif (t == "b"):
        global global_bool
        global_bool = global_bool + 1
        return global_bool
    elif (t == "s"):
        global global_string
        global_string = global_string + 1
        return global_string
    elif (t == "o"):   
        global global_object
        global_object = global_object + 1 
        return global_object

def get_next_local(t):
    if(t == "i"):
        global local_int
        local_int = local_int + 1
        return local_int
    elif (t == "f"):
        global local_float
        local_float = local_float + 1
        return local_float 
    elif (t == "b"):
        global local_bool
        local_bool = local_bool + 1
        return local_bool
    elif (t == "s"):
        global local_string
        local_string = local_string + 1
        return local_string
    elif (t == "o"):   
        global local_object
        local_object = local_object + 1 
        return local_object

def get_next_local_list(t, dim):
    print(t, memory_table[dim].value)
    dimension = memory_table[dim].value
    if(t == "i"):
        global local_int
        local_int_aux = local_int + 1
        local_int = local_int + (dimension + 1)
        return local_int_aux
    elif (t == "f"):
        global local_float
        local_float_aux = local_float + 1
        local_float = local_float + (dimension + 1)
        return local_float
    elif (t == "b"):
        global local_bool
        local_bool_aux = local_bool + 1
        local_bool = local_bool + (dimension + 1)
        return local_bool_aux
    elif (t == "s"):
        global local_string
        local_string_aux = local_string + 1
        local_string = local_string + (dimension + 1)
        return local_string_aux
    elif (t == "o"):   
        global local_object
        local_object_aux = local_object + 1
        local_object = local_object + (dimension + 1)
        return local_object_aux

def get_next_global_list(t, dim):
    print(t, memory_table[dim].value)
    dimension = memory_table[dim].value
    if(t == "i"):
        global global_int
        global_int_aux = global_int + 1
        global_int = global_int + (dimension + 1)
        return global_int_aux
    elif (t == "f"):
        global global_float
        global_float_aux = global_float + 1
        global_float = global_float + (dimension + 1)
        return global_float_aux
    elif (t == "b"):
        global global_bool
        global_bool_aux = global_bool + 1
        global_bool = global_bool + (dimension + 1)
        return global_bool_aux
    elif (t == "s"):
        global global_string
        global_string_aux = global_string + 1
        global_string = global_string + (dimension + 1)
        return global_string_aux
    elif (t == "o"):   
        global global_object
        global_object_aux = global_object + 1
        global_object = global_object + (dimension + 1)
        return global_object_aux
    
def get_next_temporal(t):
    if(t == "i"):
        global temporal_int
        temporal_int = temporal_int + 1
        return temporal_int
    elif (t == "f"):
        global temportal_float
        temportal_float = temportal_float + 1
        return temportal_float 
    elif (t == "b"):
        global temporal_bool
        temporal_bool = temporal_bool + 1
        return temporal_bool
    elif (t == "s"):
        global temporal_string
        temporal_string = temporal_string + 1
        return temporal_string
    elif (t == "o"):   
        global temporal_object
        temporal_object = temporal_object + 1 
        return temporal_object


def get_next_constant(t):
    if(t == "i"):
        global constant_int
        constant_int = constant_int + 1
        return constant_int
    elif (t == "f"):
        global constant_float
        constant_float = constant_float + 1
        return constant_float 
    elif (t == "b"):
        global constant_bool
        constant_bool = constant_bool + 1
        return constant_bool
    elif (t == "s"):
        global constant_string
        constant_string = constant_string + 1
        return constant_string
    elif (t == "o"):   
        global constant_object
        constant_object = constant_object + 1 
        return constant_object

