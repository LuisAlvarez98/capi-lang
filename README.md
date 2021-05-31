# capi-lang
![logo-lang](https://user-images.githubusercontent.com/16018384/120242736-41e76c80-c22b-11eb-8a55-a38e9bdf9e10.PNG)

Capi Lang is a game engine for 2D videogames. Our scope for this project is to build a language that has a similar structure as Typescript, C++ and others. Some of the basic
stuff you can do with Capi lang is:
- Declare variables [string,int,float,bool]
- Declare functions [string,int,float,bool,void]
- Expression Assignment
- Function Calls
- Recursive functions
- Return values from functions
- Keyboard input
- Console output
- If/Else conditions
- While/for loops
- Declare 1D Lists
- 1D Lists indexing
- 1D lists assignment
- Mathematic expressions such as sqrt and pow.
- Build 2D games with our special functions

Basic structure of Capi Lang

```
@ Global Definition of Variables

global : {
    var id: int;
};

@ Definition of functions

void func test():{

};

void func myfunc():{

};

@ Definition of main module

main :{

    @ Definition of start function - this function runs at the start of the program

    void func start():{
        test();
        print("Capi Example");
    };

    @ Definition of run function - this function is the game infinite loop

    void func run():{
        quit() @ Quit is used when you just want to execute no game related code.
    };
};


```
Declaration of variables
```
@ You can declare variables in the global section
global : {
    var integerVariable: int;
    var stringVariable: string;
    var floatVariable: float;
    var boolVariable: bool;
};

@ You can also declare variables in functions
void func myfunc():{
    var myVariable:int;
};
```
Expressions and Assignment
```
   void func start():{
        @ You can assign a value to a variable by using the '=' operator 
        @ [The value you are trying to assign must be of the same type of the variable]
        a = 3;
        b = 2;
        c = 1;
        d = 0;
        e = 32;
        f = 10;
        g = 6;
        
        @ An example of Aritmetic expressions
        res = (a + b + (c * d * (e - f * (g - 2)) + 3) * 2);
        @ An example of Logic expressions
        print((true && true) || (true || false));
        @ An example of Relational expressions
        print((5 - 2) >= (3 * 3));
        
        print("Result",res);
    };
```
Console output
```
print(expression);
print("example");
print(aVariable);
print(5 * 3);
```

Declaration of functions


Type functions and return statement

The return statement returns a value of the same type of the function.
```
@ An int function with an int parameter
int func myIntFunction(a:int):{
    return a + 10; @ Return statement
};
```

Void functions
```
@ A void function without parameters
void func myVoidFunction():{
    print("This is a void function");
};
```

When you create a function you now have access to that piece of code whenever you want. If you want to run that function you need to call it.

This concept is called function call.
```
@ Global Definition of Variables

global : {
    var aVariable: int;
};

@ Definition of functions

int func myIntFunction(a:int):{
    return a + 10;
};

@ Definition of main module

main :{

    @ Definition of start function - this function runs at the start of the program

    void func start():{
        @ Basic function call
        print(myIntFunction(5)); @ The result will be 5 + 10 = 15
    };

    @ Definition of run function - this function is the game infinite loop

    void func run():{
        quit() @ Quit is used when you just want to execute no game related code.
    };
};

```
Recursive functions example 'Factorial'
```
@ Global Definition of Variables

global : {
    var aVariable:int;
};

int func factRec(n:int):{
    if(n == 1):{
        return n;
    };else:{
        return n * factRec(n - 1);
    };
};

@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
        print("Recursive factorial");
        aVariable = 7;
        print(factRec(aVariable));
    };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        quit();
    };
};
```
Conditions
```
@ Basic structure if

if(5 > 2):{
    ...do something
};

@ Basic structure if/else

if(3 * 4 > 2 - 1):{
   ...do something if true
};else:{
   ...do something if false
};
```

Loops (for/while)
```
@ Basic for loop structure

for(i = 0; i < 10; i = i + 1;):{
    print(i);
};

@ Basic while loop structure

while(j < 10):{
    print(j);
    j = j + 1;
};
```
1 Dimension Lists

List declaration
```
var listVariable: list|int|[5];
```

List access
```
print(listVariable[2]);
```

List assignment
```
listVariable[0] = 0;
listVariable[1] = 5 * 4;
listVariable[2] = 21 - 4;
```

List basic special functions
```
listVariable.size() @ Returns the size of the list
listVariable.head() @ Returns the first element of the list.
listVariable.find(element) @ Returns True if value is in the list. Returns false otherwise.
listVariable.last() @ Returns the last element of the list.
```

Bubble sort using a list
```
@ Global Definition of Variables

global : {
    var arr:list|int|[5];
    var i,j,temp:int;
};

void func bubble(n:int):{ 
    print("bubbleSort");
    for(i = 0; i < (n - 1); i = i + 1;):{
        for(j = 0; j < (n - i - 1); j = j + 1;):{
            if(arr[j] > arr[j+1]):{
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            };
            
        };
    };
};

void func printList(n: int):{
    var x: int;
    x = 0;
    while(x < n):{
        print(arr[x]);
        x = x + 1;
    };
};


@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
        arr[0] = 3;
        arr[1] = 1;
        arr[2] = 2;
        arr[3] = 100;
        arr[4] = 5;
        print("listaAntes");
        printList(5);
        bubble(5);
        printList(5);
    };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        quit();
    };
};

```

Mathematic functions
```
pow(x,y) @ Gets the x to the y.
sqrt(x); @ Gets the square root of x.
rand(x,y) @ Generates a random number between x and y.
```

# Building 2D videogames with Capi Lang
![2021-05-31 16-57-03](https://user-images.githubusercontent.com/16018384/120245017-837b1600-c231-11eb-962c-a72e86749ac9.gif)


- Definition of tokens [✔]
- Definition of diagrams [✔]
- Definition of context free grammars [✔]
- Lex & Yacc in PLY [✔]
- Function Directory [✔]
- Tables of Variables [✔]
- Table of Semantic Considerations (designed) [✔]
- Implemented Stack to manage different scopes [✔]
- Implemented Semantic Cube [✔]
- Implemented actions to generate quadruples in arithmetic expressions [✔]
- Implemented actions to generate quadruples in logical and relational expressions [✔]
- Implemented actions to generate quadruples for print and assignments [✔]
- Implemented actions to generate quadruples for non linear statements (for,if,while) [✔]
- Implemented actions to generate quadruples for return statement [✔]
- Implemented actions to add the parameter order to the functions, quadruple count and temporal count in the function definition [✔]
- Implemented actions to generate quadruples in function calls.[✔]
- Implemented a memory handler for variable declaration and constants[✔]

