# opetusprossu
Simppeli prossusimu pythonilla  + GUI Tk:lla


## Opcodes

**mov** op1, op2
```
  op1: reg
  op2: reg or number
  op1 = op2
```


**load** op1, op2
```
  op1: reg
  op2: reg or number
  op1 = memory[ op2 ]
```

**store** op1, op2
```
  op1: reg or number
  op2: reg
  memory[ op1 ] = op2
```


**push** op1
```
  op1: reg or number
  push op1 to stack
```

**pop** op1
```
  op1: reg
  stack top to op1
```

**label** *label*
```
  create jump label
```


**inc** op1
```
  op1: reg
  op1 = op1 + 1
```

**dec** op1
```
  op1: reg
  op1 = op1 - 1
```

**add** op1, op2
```
  op1: reg
  op2: reg or number
  op1 = op1 + op2
```

**sub** op1, op2
```
  op1: reg
  op2: reg or number
  op1 = op1 - op2
```

**mul** op1, op2
```
  op1: reg
  op2: reg or number
  op1 = op1 * op2
```

**div** op1, op2
```
  op1: reg
  op2: reg or number
  op1 = op1 / op2
```

**cmp** op1, op2
```
  op1: reg
  op2: reg or number
  compares op1 and op2
```

**jmp** *label*
```
  Uncoonditional jump to label
```

**je** *label*
```
  Jump to label if last compare was equal
```

**jne** *label*
```
 Jump to label if last compare was not equal
 ```

**jg** *label*
```
Jump to label if last compare greater
```

**out** op1
```
  op1: reg or number
  send byte to output
```
