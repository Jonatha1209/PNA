# PNA

pna is a custom scripting language with a simple, readable syntax designed to define variables, objects, conditionals, loops, and logging output. It supports built-in functions, input/output, and flow control structures like if, loop, break, and continue.

## Variable Definition
### object style devlaration

```pna
enemy: {
    name: "Slime",
    hp: 100,
}
```

- Defines a dictionary-style variable enemy with properties name and hp.

## Assignment
### Assign to a field:
```pna
enemy.hp: 75
```
- Sets the hp field of enemy to 75.

### Arithmetic and expressions are supported:
```pna
enemy.hp: enemy.hp - 10
```

## Looping

### Log to console :

```pna
log "Hello"
log "HP: " + str(enemy.hp)
```

- Strings can be concatenated with +.
- str() converts other types to string for logging.

## Built-in Functions

Pna supports various built-in functions:
```pna
randint 1 10       // Random int from 1 to 10
str(123)           // Convert to string
int("123")         // Convert to integer
len("abc")         // Length of string
not true           // Boolean not
inlist "a" "a,b,c" // True
```


## Input

### Get user input :

```pna
input "What is your name?" -> player.name
```

- Asks the question and stores input into player.name.

### If no prompt:

```pna
input -> player.age
```

- Equivalent to input() in python.

## Conditionals

### If-style block:

```pna
cond (enemy.hp <= 0) -> {
    log "Enemy defeated!"
} end
```

- If condition is true, the block runs.

## Loops

### loop block with condition:

```pna
loop (anycondition) -> {
    log "Repeating"
    break
} end```

- Runs while the condition is true.

### Supports break and continue:

```pna
break       // exits the loop
continue    // skips to next iteration
```
