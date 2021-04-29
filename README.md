# capi-lang
Game Engine for 2D videogames

Basic structure of Capi Lang ->

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
        draw("blue", "yellow");
        print(size() + 2 );
    };

    @ Definition of run function - this function is the game infinite loop

    void func run():{
        print(5 + 5);
        for(i = 5; i >= 0; i = i - 1;):{
            print(i);
        };
    };
};


```

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

