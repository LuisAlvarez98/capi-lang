
from memory import  memory_table,print_const_table, memory,constant_table, init_memory, call_stack, function_list, GLOBAL_START, LOCAL_START, TEMPORAL_START, CONSTANT_START

cont = 0

def init_virtual(quadruples, func_dir):

    init_memory(func_dir)
    global cont
    while cont < len(quadruples):
        action(quadruples[cont])
        cont+=1
    print(call_stack)

def action(quadruple):
    global cont
    print("Running quadruple: ", cont, quadruple)
    if quadruple.operator == '+':
        temp = get_value(quadruple.left_operand).value + get_value(quadruple.right_operand).value
        call_stack[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '-':
        temp = get_value(quadruple.left_operand).value - get_value(quadruple.right_operand).value
        call_stack[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '*':
        temp = get_value(quadruple.left_operand).value * get_value(quadruple.right_operand).value
        call_stack[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '/':
        temp = get_value(quadruple.left_operand).value / get_value(quadruple.right_operand).value
        call_stack[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '=':
        if quadruple.temp not in call_stack[-1].memory_list:
            set_global_var(quadruple.temp, get_value(quadruple.left_operand).value)
        else:
            call_stack[-1].memory_list[quadruple.temp].value = get_value(quadruple.left_operand).value
    elif quadruple.operator == 'print':
        print(get_value(quadruple.temp).value)
    elif quadruple.operator == 'GOTO':
        cont = quadruple.temp - 1
    elif quadruple.operator == 'ERA':
        # We push the context into the call_stack
        call_stack.append(function_list[quadruple.left_operand])
    elif quadruple.operator == 'ENDFUNC':
        # It checks if the function is not run and start so that the cont does not reset. 
        if call_stack[-1].function_name != "run" and call_stack[-1].function_name != "start" :
            cont = call_stack[-1].prev - 1
        call_stack.pop()
    elif quadruple.operator == 'GOSUB':
        #we store the previous position
        call_stack[-1].prev = cont + 1
        cont = call_stack[-1].cont - 1


# function used to get value from different scopes
def get_value(address):
    if address >= CONSTANT_START:
        return memory_table[address]
    elif address >= LOCAL_START and address <= CONSTANT_START - 1:
        memory_list = call_stack[-1].memory_list
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

