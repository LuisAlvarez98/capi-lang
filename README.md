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
# Run Capi code
To run .capi code you must create a .capi file in the /tests folder and run this command:

```
python capi.py -f "tests/code.capi"
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

# Capigame Functions
```
capigame.init() @ This will init the game environment.
capigame.draw(color,x,y,width,height); @ This is used to draw a figure in the window.
capigame.set_fill(r,g,b); @ Sets the color of the window
capigame.get_event(); @ Gets the events of the game
capigame.set_dimension(width,height);  @ Sets the dimension of the window
capigame.set_title("Title"); @ Sets the title of the window
capigame.update(); @ Updates the window frames
capigame.window_h(); @ Gets the window height
capigame.window_w(); @ Gets the window width
create_text("Title", color, x,y); @ Creates a text object in the game window.
quit(); # Quits the game.
```

# Capigame Colors
Available colors:
- BLUE
- GREEN
- RED
- YELLOW
- ORANGE
- PINK
- GREY
- WHITE
- BLACK
- CYAN

# Capigame Events
- KEYUP 
- KEYDOWN
- KEYLEFT
- KEYRIGHT
- KEYESCAPE

# Basic game setup
Capi Lang was created so that anyone with some coding skills can build a 2D basic game.

In this section we will explain how to build a game from scratch using capi lang.

The first step is to create a .capi file with this structure:
```
@ Global Definition of Variables
global : {
};

@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{

   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{

    };
};
```
We will introduce capi functions in this section:

To start creating videogames you will need to first initiate the video game. To do this you can simply call the function:
```
void func start():{
    capigame.init(); @This function must be called in the start module, this will init the game environment.
};
```

The next step is to create a window for you videogame:

The way of doing this is by using the function set_dimension.
```
void func start():{
    capigame.init(); @This function must be called in the start module, this will init the game environment.
    capigame.set_dimension(700,500); @ The parameters are width and height of the window.
    @ You can also set the title of the window.
};
```
Setting a title to our videogame
```
void func start():{
    capigame.init(); @This function must be called in the start module, this will init the game environment.
    capigame.set_dimension(700,500); @ The parameters are width and height of the window.
    @ You can also set the title of the window.
    capigame.set_title("My videogame");
};
```
Setting a color to our background
```
@ Definition of run function - this function is the game infinite loop
void func run():{
    capigame.set_fill(255,0,0);
    capigame.update(); @ This function is important because it will help the game to keep updated each frame.
};
```
If we combine everything we should get this
```
@ Global Definition of Variables

global : {
};


@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
       @ We init the game
       capigame.init();
       @ We setup the dimension of the window
       capigame.set_dimension(700,500);
       @ We set the title of the window
       capigame.set_title("My videogame");
   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        capigame.set_fill(255,0,0);
        capigame.update();
    };
};
```
Output:<br/>
![image](https://user-images.githubusercontent.com/16018384/120245770-e8377000-c233-11eb-996e-d4e2dc48c678.png)
# Adding a player to our videogame

In this section we will introduce some concepts that will be usefull when creating a videogame with Capi Lang.

We will create two variables 
```
var xPosition:int;
var yPosition:int;
```
We will integrate this code to our base code:
```
@ Global Definition of Variables

global : {
var xPosition:int;
var yPosition:int;
};


@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
       @ We init the game
       capigame.init();
       @ We setup the dimension of the window
       capigame.set_dimension(700,500);
       @ We set the title of the window
       capigame.set_title("My videogame");
   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        capigame.set_fill(255,0,0);
        capigame.update();
    };
};
```
Then we will assign a 0 to the variables ```xPosition``` and ```yPosition```
```
@ Global Definition of Variables

global : {
var xPosition:int;
var yPosition:int;
};


@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
       @ We init the game
       capigame.init();
       @ We setup the dimension of the window
       capigame.set_dimension(700,500);
       @ We set the title of the window
       capigame.set_title("My videogame");
       
       xPosition = 0;
       yPosition = 0;
       
   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        capigame.set_fill(255,0,0);
        capigame.update();
    };
};
```
Now that we have our position variables created we will now create our player. We will need to create a function
so that we can draw our player in our window. We will be using another capigame function called ```capigame.draw(color,x,y,width,height);```

In Capi Lang we have several colors, we encourage you to read that section.

We create this function called drawPlayer
```
@ Function used to draw a player
void func drawPlayer(x:int, y:int):{
    capigame.draw("GREEN",x,y,50,50); 
    @ This function will draw a figure with color "GREEN" at position x and y. The width/height of the figure will be 50x50
};
```

After creating our function we integrate the code this way.

```
@ Global Definition of Variables

global : {
var xPosition:int;
var yPosition:int;
};

void func drawPlayer(x:int, y:int):{
    capigame.draw("GREEN",x,y,50,50); 
    @ This function will draw a figure with color "GREEN" at position x and y. The width/height of the figure will be 50x50
};

@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
       @ We init the game
       capigame.init();
       @ We setup the dimension of the window
       capigame.set_dimension(700,500);
       @ We set the title of the window
       capigame.set_title("My videogame");
       
       xPosition = 0;
       yPosition = 0;
       
   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        capigame.set_fill(255,0,0);
        drawPlayer(xPosition, yPosition);
        capigame.update();
    };
};
```
Output:<br/>
![image](https://user-images.githubusercontent.com/16018384/120246320-811abb00-c235-11eb-870c-34155ba32c76.png)
# Events in Capi Lang
We will intoduce an important concept that is an Event.
When creating a game with Capi Lang there will be plenty of events occurring in the run function. Some example of those events are:
- Keyboard inputs
- Quit input 

We will use this events to move our player and we will need to run another capigame function called ```capigame.get_event();```
That function will obtain all the events occurring in the run function.

We will first create a string variable that will store the current event
```
var event: string;
```
Then we will initialize our event variable in the run function like this:
```
event = capigame.get_event(); @ This value will be changing depending of the event that is currently happening.
```
The next step is to integrate this into our game code:
```
@ Global Definition of Variables

global : {
var xPosition:int;
var yPosition:int;
var event: string;
};

void func drawPlayer(x:int, y:int):{
    capigame.draw("GREEN",x,y,50,50); 
    @ This function will draw a figure with color "GREEN" at position x and y. The width/height of the figure will be 50x50
};

@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
       @ We init the game
       capigame.init();
       @ We setup the dimension of the window
       capigame.set_dimension(700,500);
       @ We set the title of the window
       capigame.set_title("My videogame");
       
       xPosition = 0;
       yPosition = 0;
       
   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        capigame.set_fill(255,0,0);
        event = capigame.get_event();
        
        drawPlayer(xPosition, yPosition);
        capigame.update();
    };
};
```
Now we will add some events so that we can handle our player movement.
Some of the events that can be used in Capi Lang will be listed in the event section.
We will be using ```KEYLEFT, KEYRIGHT, KEYUP, KEYDOWN```

```
@ Global Definition of Variables

global : {
var xPosition:int;
var yPosition:int;
var event: string;
};

void func drawPlayer(x:int, y:int):{
    capigame.draw("GREEN",x,y,50,50); 
    @ This function will draw a figure with color "GREEN" at position x and y. The width/height of the figure will be 50x50
};

@ Definition of main module
main :{
    @ Definition of start function - this function runs at the start of the program
    void func start():{
       @ We init the game
       capigame.init();
       @ We setup the dimension of the window
       capigame.set_dimension(700,500);
       @ We set the title of the window
       capigame.set_title("My videogame");
       
       xPosition = 0;
       yPosition = 0;
       
   };

    @ Definition of run function - this function is the game infinite loop
    void func run():{
        capigame.set_fill(255,0,0);
        event = capigame.get_event();
        @ We use an if statement so that we can handle the events
        if(event == "KEYLEFT"):{
            xPosition = xPosition - 1; @ This will move the player to the left
        };
        if(event == "KEYRIGHT"):{
            xPosition = xPosition + 1;  @ This will move the player to the right
        };
        if(event == "KEYUP"):{
            yPosition = yPosition - 1;  @ This will move the player up
        };
        if(event == "KEYDOWN"):{
            yPosition = yPosition + 1; @ This will move the player down
        };
       
        drawPlayer(xPosition, yPosition);
        capigame.update();
    };
};
```
Output:<br/>
![2021-05-31 17-42-59](https://user-images.githubusercontent.com/16018384/120247036-c2ac6580-c237-11eb-8acf-da1de4901a57.gif)
