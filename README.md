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
