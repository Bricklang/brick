let's get started with the language style, syntax and grammar:
## Functions
```brick
fn add(x::i32,y::i32)->i32 {
     ret x+y;
} 
```

## Comments
```brick
:> This is a comment <:
```

## Variables
```brick
val x::i32 = 10;
val mystr::String = "Hello, World!";
val myarr::[i32] = {0,1,2,3,4,5,6,7,8,9};
```

## Condition
```brick
if (x==1)? {
    println("X is 1");
}

&if (x==2) {
    println("X is 2);
}

else {
    println("X is something");
}
switch (x) {
    case 1 {
        println("X is 1");
    }
    case 2 {
        println("X is 2);
    }
    case default {
        println("X is something");
    }
}
```

## Keywords
All default keywords that are builtin every programming language

## Classes
```brick
class myclass {
    fn add(x::i32,y::i32)-> i32 {
        ret x+y;
    }
}
```

## Libs/Modules and files/Modules
You can combine Import as and From Import

### Just import
Functions will be accessible by using `libname.function_name()`
```brick
get {                    >> Libraries
    "myfirstlib",
    "mysecondlib"
}

include {                >> Files
    "myfile"             >> In my root dir there's myfile.brick
}
```

### Import as
Functions will be accessible by using "asname.function_name()`
```brick
get {                    >> Libraries
    "myfirstlib": "custom_name,
    "mysecondlib": "lib_name"
}

include {                >> Files
    "myfile": "custom_file_name"
}
```

### From Import
Functions will be accessible by using `function_name()`
```brick
get {                    >> Libraries
    "myfirstlib.function_name",
    "mysecondlib.myfunction",
}

include {                >> Files
    "myfile.add",
}
```


### Error Handling
```brick
try {
    my_function()
}
except {
    println("My function run failed")
}
```


## Garbage Collector
Variables and functions don't have a lifetime
but if they aren't used from long time they will automatically deleted from memory


## Overloading Operators
```brick
x=40
x++       >> x=41
```

```brick
x=40
x+=1      >> x=41
```

```brick
x=40
x--      >> x=39
```

```brick
x=40
x*=2     >> 80
```

```brick
x=40
x/=2     >> 20
```


## Concurrency 
No threading or race condition