
from memory import  memory_table, memory,constant_table, init_memory,create_func_memory, call_stack, function_list,func_memory, GLOBAL_START, LOCAL_START, TEMPORAL_START, CONSTANT_START
from time import sleep
import math
from collections import deque
import pygame
cont = 0 # Quadruple counter
current_context = func_memory() # We use this to handle the current context
visitedFuncs = deque() # We use this to handle visited functions

screen = None
clock = pygame.time.Clock()

colors ={
    "\"BLUE\"": (0,0,255),
    "\"GREEN\"": (0,255,0),
    "\"RED\"": (255,0,0),
}

events={}

class capi_object():
    def __init__(self, screen,color, x, y, w, h, address):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.address = address
        def draw_object():
            pygame.draw.rect(self.screen,self.color,(self.x,self.y,self.w,self.h))
        self.draw_object = draw_object
    def __str__(self):
        return f'Color: {self.color}, x: {self.x}, y: {self.y}, w: {self.w}, h:{self.h}, Address: {self.address}\n'
    def __repr__(self):
        return f'Color: {self.color}, x: {self.x}, y: {self.y}, w: {self.w}, h:{self.h}, Address: {self.address}\n'



def init_virtual(quadruples, func_dir):
    global current_context,cont
    for i, q in enumerate(quadruples):
        print(i, " ", q)

    init_memory(func_dir)
    current_context = call_stack[-1]
    # We use this to loop through the quadruples
    while cont < len(quadruples):
        action(quadruples[cont])
        cont+=1

# We handle the quadruple with this function
def action(quadruple):
    global cont, current_context, screen, clock
    #print("Running quad: ", cont, " ", quadruple)
    if quadruple.operator == '+':
        if quadruple.isptr:
            temp = get_value_visited_func(quadruple.left_operand).value + get_value_visited_func(quadruple.right_operand).value
            value_from_pointer = get_value_visited_func(temp + 1).value 
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(value_from_pointer, quadruple.temp)
        else:
            temp = get_value_visited_func(quadruple.left_operand).value + get_value_visited_func(quadruple.right_operand).value
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '-':
        temp = get_value_visited_func(quadruple.left_operand).value - get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '*':
        temp = get_value_visited_func(quadruple.left_operand).value * get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '/':
        temp = get_value_visited_func(quadruple.left_operand).value / get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '&&':
        temp = get_value_visited_func(quadruple.left_operand).value and get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '||':
        temp = get_value_visited_func(quadruple.left_operand).value or get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '>=':
        temp = get_value_visited_func(quadruple.left_operand).value >= get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '<=':
        temp = get_value_visited_func(quadruple.left_operand).value <= get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '>':
        temp = get_value_visited_func(quadruple.left_operand).value > get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '<':
        temp = get_value_visited_func(quadruple.left_operand).value < get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '!=':
        temp = get_value_visited_func(quadruple.left_operand).value != get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == '==':
        temp = get_value_visited_func(quadruple.left_operand).value == get_value_visited_func(quadruple.right_operand).value
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(temp, quadruple.temp)
    elif quadruple.operator == 'VERIFY':
        index = get_value_visited_func(quadruple.left_operand).value
        lower_bound = get_value_visited_func(quadruple.right_operand).value
        upper_bound = get_value_visited_func(quadruple.temp).value 
        if index >= upper_bound or index < lower_bound:
            raise Exception("Index out of bounds.")
    elif quadruple.operator == '=':
        if quadruple.isptr:
            # We obtain the list address
            list_address = quadruple.temp
            # We get the value of the list addres and that is our address of our list.
            index = get_value_visited_func(list_address).value + 1 # we add up one to get into the correct address.
            if index not in visitedFuncs[-1].memory_list:
                set_global_var(index, get_value_visited_func(quadruple.left_operand).value)
            else:
                visitedFuncs[-1].memory_list[index].value = get_value_visited_func(quadruple.left_operand).value
        else:
            if quadruple.temp >= GLOBAL_START and quadruple.temp <= LOCAL_START - 1:
                set_global_var(quadruple.temp, get_value_visited_func(quadruple.left_operand).value)
            else:
                if quadruple.temp not in visitedFuncs[-1].memory_list:
                    visitedFuncs[-1].memory_list[quadruple.temp] = memory(get_value_visited_func(quadruple.left_operand).value, quadruple.temp)
                else:
                    visitedFuncs[-1].memory_list[quadruple.temp].value = get_value_visited_func(quadruple.left_operand).value

    elif quadruple.operator == 'SIZE':
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(get_value_visited_func(quadruple.left_operand).value, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = get_value_visited_func(quadruple.left_operand).value
    elif quadruple.operator == 'HEAD':
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(get_value_visited_func(quadruple.left_operand + 1).value, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = get_value_visited_func(quadruple.left_operand + 1).value
    elif quadruple.operator == 'INIT':
        print("Pygame was initialized")
        pygame.init()
    elif quadruple.operator == 'SET_DIM':
        screen = pygame.display.set_mode((get_value_visited_func(quadruple.left_operand).value,get_value_visited_func(quadruple.right_operand).value))
    elif quadruple.operator == 'SET_TITLE':
        pygame.display.set_caption(get_value_visited_func(quadruple.left_operand).value)
    elif quadruple.operator == 'SET_FILL':
        screen.fill((get_value_visited_func(quadruple.left_operand).value, get_value_visited_func(quadruple.right_operand).value, get_value_visited_func(quadruple.temp).value))
    elif quadruple.operator == 'UPDATE':
        pygame.display.flip() #Draws the objects in pygame
        pygame.display.update() # Updates the frames
    elif quadruple.operator =='CREATE_TEXT':
        font = pygame.font.Font('freesansbold.ttf', 32)
        color = colors[get_value_visited_func(quadruple.right_operand[0]).value]
        x = get_value_visited_func(quadruple.right_operand[1]).value
        y = get_value_visited_func(quadruple.right_operand[2]).value
        text = get_value_visited_func(quadruple.left_operand).value
        text_obj = font.render(text, True, color)
        screen.blit(text_obj,(x,y))
    elif quadruple.operator == 'DRAW':
        color = colors[get_value_visited_func(quadruple.left_operand).value]
        x = get_value_visited_func(quadruple.right_operand[0]).value
        y = get_value_visited_func(quadruple.right_operand[1]).value
        w = get_value_visited_func(quadruple.right_operand[2]).value
        h = get_value_visited_func(quadruple.right_operand[3]).value
        c = capi_object(screen, color, x,y,w,h,quadruple.temp)
        # We add our object to our memory list
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(c, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = c
        # We draw the object
        c.draw_object()
    elif quadruple.operator == 'POW':
        num = get_value_visited_func(quadruple.left_operand).value
        pot = get_value_visited_func(quadruple.right_operand).value
        result = math.pow(num,pot)
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(result, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = result
    elif quadruple.operator == 'SQRT':
        num = get_value_visited_func(quadruple.left_operand).value
        result = math.sqrt(num)
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(result, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = result
    elif quadruple.operator == 'GET_EVENT':
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    handle_event(quadruple, "\"KEYLEFT\"")
                if event.key == pygame.K_RIGHT:
                    handle_event(quadruple, "\"KEYRIGHT\"")
                if event.key == pygame.K_UP:
                    handle_event(quadruple, "\"KEYUP\"")
                if event.key == pygame.K_DOWN:
                    handle_event(quadruple, "\"KEYDOWN\"")
                if event.key == pygame.K_SPACE:
                    print("space")
                    handle_event(quadruple, "\"KEYSPACE\"")
            else:
                handle_event(quadruple, "\"NULL\"")
            # We use this so that the user can quit the game
            if event.type == pygame.QUIT:
                print("Game terminated. Thank you for using Capi :)")
                exit()
    elif quadruple.operator == 'WINDOW_H':
        x,y = screen.get_size()
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(y, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = y
    elif quadruple.operator == 'WINDOW_W':
        x,y = screen.get_size()
        if quadruple.temp not in visitedFuncs[-1].memory_list:
            visitedFuncs[-1].memory_list[quadruple.temp] = memory(x, quadruple.temp)
        else:
            visitedFuncs[-1].memory_list[quadruple.temp].value = x
    elif quadruple.operator == 'print':
        print(get_value_visited_func(quadruple.temp).value)
    elif quadruple.operator == 'GOTO':
        cont = quadruple.temp - 1
    elif quadruple.operator == 'GOTO_F':
        if not get_value_visited_func(quadruple.left_operand).value:
            cont = quadruple.temp - 1
    elif quadruple.operator == 'PARAM':
        param_index = int(quadruple.temp.split(" ")[1]) - 1
        call_stack[-1].params[param_index].value = get_value_visited_func(quadruple.left_operand).value
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

def handle_event(quadruple, action):
    if quadruple.temp not in visitedFuncs[-1].memory_list:
        visitedFuncs[-1].memory_list[quadruple.temp] = memory(action, quadruple.temp)
    else:
        visitedFuncs[-1].memory_list[quadruple.temp].value = action
    
# function used to get value from different scopes
def get_value(address):
    global  current_context
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
    global  current_context
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
    