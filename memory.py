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



class memory():
    def __init__(self, value='', address=''):
        self.value = value
        self.address= address
    def __str__(self):
        return f'Value: {self.value}, Addr: {self.address}\n'
    def __repr__(self):
        return f'Value: {self.value}, Addr: {self.address}\n'

constant_table = {}
memory_table = {}

def get_const_address(value, type):
    if value in constant_table.keys():
        return constant_table[value].address
    address = get_next_local(type)
    new_value = memory(value, address)
    constant_table[value] =  new_value
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

def print_const_table():
    print(constant_table)