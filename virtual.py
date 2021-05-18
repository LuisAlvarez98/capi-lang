
from memory import  memory_table,print_const_table, memory

cont = 0
def init_virtual(quadruples):
    global cont
    print_const_table()
    while cont < len(quadruples):
        action(quadruples[cont])
        cont+=1
    print(memory_table)
def action(quadruple):
    global cont
    print("Running quadruple: ", cont, quadruple)
    if quadruple.operator == '+':
        temp = memory_table[quadruple.left_operand].value + memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '-':
        temp = memory_table[quadruple.left_operand].value - memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '*':
        temp = memory_table[quadruple.left_operand].value * memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '/':
        temp = memory_table[quadruple.left_operand].value / memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == 'print':
        print("Printing: " , memory_table[quadruple.temp].value) 
    elif quadruple.operator == '=':
        memory_table[quadruple.temp] = memory(memory_table[quadruple.left_operand].value, quadruple.temp)
    elif quadruple.operator == 'GOTO':
        cont = quadruple.temp - 1