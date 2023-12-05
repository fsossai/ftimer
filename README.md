# FTimer
Time your python scripts easily and with style. This tool uses [`flog`](https://github.com/fsossai/flog) to format its output.

The same classes can be used either through `with` or as a `@decorator`.

## Example

```python
import ftimer
import flog
import time

@ftimer.section("Factorial computation", tail="Took {}")
def fact(n):
    if n == 1:
        flog.log("Reached base case")
        return 1
    flog.log("This is not the base case")
    with ftimer.step("Sleeping for a second"):
        time.sleep(1)
    res = n * fact(n-1)
    return res

ftimer.unit = "s" # or "ms", "us", "m", "h"
fact(4)
```
Will produce the following **output**:
```
┌─ Factorial computation
│  This is not the base case
│  Sleeping for a second ... done in 1.001 s
│  ┌─ Factorial computation
│  │  This is not the base case
│  │  Sleeping for a second ... done in 1.003 s
│  │  ┌─ Factorial computation
│  │  │  This is not the base case
│  │  │  Sleeping for a second ... done in 1.002 s
│  │  │  ┌─ Factorial computation
│  │  │  │  Reached base case
│  │  │  └─ Took 0.000 s
│  │  └─ Took 1.003 s
│  └─ Took 2.006 s
└─ Took 3.007 s
```

## Features

### `ftimer.tracker()` 
Prints the description and the elapsed time in the same line. It is suggested for code sections that don't print any output.

  As a context:
```python
with ftimer.step("Inverting the matrix"):
  B = np.linalg.inv(A)
```
As a decorator:
```python
@ftimer.step("Inverting the matrix"):
def inv(A):
  return np.linalg.inv(A)
```
Will produce something like `Invering the matrix ... took 0.123 s`.

### `ftimer.section()`
It's useful when timing complex code with nested calls to other timed functions.

As a decorator:
```python
@ftimer.section():
def inv(A):
  return np.linalg.inv(A)
```
As a context:
```python
@ftimer.section()
def parse(file_name):
    flog.log("File name:", file_name)
    return None

@ftimer.section()
def count_words(d):
    return 0

@ftimer.section()
def main():
    d = parse("words.txt")
    n = count_words(d)
    flog.log(n)
```
Will produce something like
```
┌─ main
│  ┌─ parse
│  │  File name: words.txt
│  └─ parse: 0.123 s
│  ┌─ count_words
│  └─ count_words: 4.567 s
└─ main: 4.701 s
```

### `ftimer.flat()`
It's useful when timing code that prints text and we want the output to be flat (no indentation).

As a decorator:
```python
@ftimer.flat():
def inv(A):
  return np.linalg.inv(A)
```
 As a context:
```python
with ftimer.flat("inv"):
  B = np.linalg.inv(A)
```
Will produce something like
```
[*] inv
[*] inv: 0.123 s
```



