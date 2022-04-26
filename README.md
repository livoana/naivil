# User Guide

## Installation and Run Instructions

In order to run NAIVIL properly a few steps have to pe made:

1.  Download NAIVIL from the GitHub repository
    **https://github.com/livoana/naivil**.

2.  Run **NaivilDependenciesDownload.ps1** that downloads and installs
    all the required packages.

3.  Write a piece of code in NAIVIL and save the file into the root
    folder

4.  Run the compiler with the naivilRun**.ps1 \[filename\]**.

After the run is complete in the root folder you will find a folder with
the name **\[filename\].build** that contains the executable and, also,
the LLVM listing.

## Coding Instructions

### **main()** method

NAIVIL uses the **main()** method as an entry point so it is required to
exist at any times. Every function declaration has to end with a
semicolon.

``` {.objectivec language="C"}
func void main(){
//Some code here
};
```

### Variable declaration

Since NAIVIL has statically typed variables, the variables declaration
should contain the variable name and also the type of variable. Also the
declaration of variables should end with a semicolon.

``` {.objectivec language="C"}
var a int64;
var b str;
var c float;
var e int128;
var f bigint;
```

At this time the only available variable types are :

``` {.objectivec language="C"}
int32 //32 bit Signed Integer -2147483648 to 2147483647
int64 //64 bit Signed Integer -9223372036854775808 to 9223372036854775807
int128 //128 bit Signed Integer -170141183460469231731687303715884105728 to 170141183460469231731687303715884105727
bigint //255 bit Signed Integer
float //64 Bit Float
str //Str stands for string variables wich allocates a pointer in memory for the variable to be stored.
void //Void is a pseudo variable type that indicates the function dose not have a return value
```

The advantages of statically typed variables is that memory used is
close to the actual memory required and also that stack overflows and
buffer overruns are less likely to appear.

### **print()** function

The **print()** method is the way that NAIVIL can output any results to
the console!It can take any type of arguments.

``` {.objectivec language="C"}
var message str;
message = "Hello Naivil!";
print(message);\\Print with string argument
>>Hello Naivil
print(125);\\Print with integer argument
>>125
print(0.685);\\Print with float argument
>>0.685
print(function(245);\\Print with function call argument
>>the result of the function call
```

### **if statement** 

The if statement is one of the building blocks of any program. It is the
way that the computer can check if a condition is **true** of **false**
and execute code accordingly.

``` {.objectivec language="C"}
var a int64;
a=100;
if (a>0){
    print("a is greater then 0");
}else{
    print("a is less then 0");
}
```

For the condition of the **if statement** there are a few possible
operators, **\<=,\>=,==,!=,\<,\>** This list of operators covers all the
possible cases of conditions.

### **while loop** 

The as with the **if statement** the **while loop** is a conditional
loop that check at every pass that a condition is **true** and executes
a piece of code accordingly

``` {.objectivec language="C"}
var a int64;
a=100;
while (a>0){
    print(a);
    a = a-1;
}
```

### **for loop** 

The **for loop** is the last of the basic blocks implemented in NAIVIL.
This loop passes an **index** though all the values indicated in a range
and executes a piece of code for each pass.

``` {.objectivec language="C"}
var a int64;
a=100;
for(i in range(0,100)){
    a=a-i;
    print(a);
}
```

### The **rust** tag 

The **rust** tag allows you to integrate in the NAIVIL code a piece of
rust textual code.

``` {.objectivec language="C"}
// rust code
rust "use factorial::Factorial;"
var x int64;
x=1;
for (a in range(0.100)){
    //rust code
    rust"println!("{}",x.factorial());"
    //naivil code
    x=x+1;
}
```
