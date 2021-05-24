
from memory import  memory_table,print_const_table, memory,constant_table, init_memory,create_func_memory, call_stack, function_list,func_memory, GLOBAL_START, LOCAL_START, TEMPORAL_START, CONSTANT_START
from time import sleep
from collections import deque
cont = 0
param_pointer = 0
current_context = func_memory()
quad = []
visitedFuncs = deque()
def init_virtual(quadruples, func_dir):
    global current_context,cont
    # for i, q in enumerate(quadruples):
    #     print(i, " ", q)

    init_memory(func_dir)
    print(func_dir)
    current_context = call_stack[-1]
    while cont < len(quadruples):
        action(quadruples[cont])
        cont+=1
def action(quadruple):
    global cont, param_pointer, current_context, quad
    print("Running ", cont, " ", quadruple)
    if quadruple.operator == '+':
        temp = get_value_visited_func(quadruple.left_operand).value + get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '-':
        temp = get_value_visited_func(quadruple.left_operand).value - get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '*':
        temp = get_value_visited_func(quadruple.left_operand).value * get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '/':
        temp = get_value_visited_func(quadruple.left_operand).value / get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '&&':
        temp = get_value_visited_func(quadruple.left_operand).value and get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '||':
        temp = get_value_visited_func(quadruple.left_operand).value or get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)

    elif quadruple.operator == '>=':
        temp = get_value_visited_func(quadruple.left_operand).value >= get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '<=':
        temp = get_value_visited_func(quadruple.left_operand).value <= get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '>':
        temp = get_value_visited_func(quadruple.left_operand).value > get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '<':
        temp = get_value_visited_func(quadruple.left_operand).value < get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '!=':
        temp = get_value_visited_func(quadruple.left_operand).value != get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '==':
        temp = get_value_visited_func(quadruple.left_operand).value == get_value_visited_func(quadruple.right_operand).value
        current_context.memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '=':
        if quadruple.temp not in current_context.memory_list:
            set_global_var(quadruple.temp, get_value(quadruple.left_operand).value)
        else:
            current_context.memory_list[quadruple.temp].value = get_value(quadruple.left_operand).value
    elif quadruple.operator == 'print':
        print(get_value(quadruple.temp).value)
    elif quadruple.operator == 'GOTO':
        cont = quadruple.temp - 1
    elif quadruple.operator == 'GOTO_F':
        if not get_value(quadruple.left_operand).value:
            cont = quadruple.temp - 1
    elif quadruple.operator == 'PARAM':
        param_index = int(quadruple.temp.split(" ")[1]) - 1
        call_stack[-1].params[param_index].value = get_value(quadruple.left_operand).value
    elif quadruple.operator == 'ERA':
        # We push the context into the call_stack
        new_func = create_func_memory(quadruple.left_operand)
        call_stack.append(new_func)
    elif quadruple.operator == 'ENDFUNC':
        # It checks if the function is not run and start so that the cont does not reset.
        if visitedFuncs:
            visitedFuncs.pop()
        current_context = call_stack[-1] #-1 -> top()
        if current_context.function_name != "run" and current_context.function_name != "start" :
            cont = current_context.prev
        call_stack.pop()
       
    elif quadruple.operator == 'GOSUB':
        visitedFuncs.append(call_stack[-1])
        current_context = call_stack[-1]
        current_context.prev = cont 
        cont = current_context.cont
    
       

# function used to get value from different scopes
def get_value(address):
    global param_pointer, current_context
    if address >= CONSTANT_START:
        return memory_table[address]
    elif address >= LOCAL_START and address <= CONSTANT_START - 1:
        memory_list = current_context.memory_list
        params_list = current_context.params
        if address not in memory_list:
            for p in params_list.values():
                if p.address == address:
                    return p
        return memory_list[address]
    elif address >= GLOBAL_START and address <= LOCAL_START - 1:
        value = None
        for p in call_stack:
            if p.function_name == "global":
                return p.memory_list[address]
        return value
# function used to get value from different scopes
def get_value_visited_func(address):
    global param_pointer, current_context
    if address >= CONSTANT_START:
        return memory_table[address]
    elif address >= LOCAL_START and address <= CONSTANT_START - 1:
        memory_list = visitedFuncs[-1].memory_list
        params_list = visitedFuncs[-1].params
        if address not in memory_list:
            for p in params_list.values():
                if p.address == address:
                    return p
        # this is used when the assign is created at the end of the function call
        if address not in memory_list.keys():
            return get_global_var(address)
        return memory_list[address]
    elif address >= GLOBAL_START and address <= LOCAL_START - 1:
        value = None
        for p in call_stack:
            if p.function_name == "global":
                return p.memory_list[address]
        return value
# function used in assign to set in global scope when the variables does not exist in current.
def set_global_var(address,value):
    for p in call_stack:
        if p.function_name == "global":
            p.memory_list[address] = memory(value,address)

def get_global_var(address):
     for p in call_stack:
        if p.function_name == "global":
            return p.memory_list[address]