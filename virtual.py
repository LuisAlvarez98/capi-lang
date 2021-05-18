
from memory import  memory_table,print_const_table


cont = 0
def init_virtual(quadruples):
    global cont
    print_const_table()
    while cont < len(quadruples)-1:
        action(quadruples[cont])
        cont+=1

def action(quadruple):
    if quadruple.operator == '+':
        temp = memory_table[quadruple.left_operand].value + memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = temp
    elif quadruple.operator == '-':
        temp = memory_table[quadruple.left_operand].value - memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = temp
    elif quadruple.operator == '*':
        temp = memory_table[quadruple.left_operand].value * memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = temp
    elif quadruple.operator == '/':
        temp = memory_table[quadruple.left_operand].value / memory_table[quadruple.right_operand].value
        memory_table[quadruple.temp] = temp
    elif quadruple.operator == 'print':
        print(memory_table[quadruple.temp]) 
