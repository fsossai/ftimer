# FTimer
Time your python scripts easily and with style. This tool uses [`flog`](https://github.com/fsossai/flog) to format its output.

The same classes can be used either through `with` or as a `@decorator`.

## Example

```python
import ftimer
import flog
import time

@ftimer.section("Factorial computation")
def fact(n):
    if n == 1:
        flog.log("Reached base case")
        return 1
    flog.log("This is not the base case")
    with ftimer.tracker("Sleeping for a second"):
        time.sleep(1)
    res = n * fact(n-1)
    return res

ftimer.unit = "s" # or "ms", "us", "m", "h"
fact(4)
```
Will produce the following **output**:
```
┌─Factorial computation
│ This is not the base case
│ Sleeping for a second ... took 1.000 s
│ ┌─Factorial computation
│ │ This is not the base case
│ │ Sleeping for a second ... took 1.005 s
│ │ ┌─Factorial computation
│ │ │ This is not the base case
│ │ │ Sleeping for a second ... took 1.004 s
│ │ │ ┌─Factorial computation
│ │ │ │ Reached base case
│ │ │ └─Elapsed: 0.000 s
│ │ └─Elapsed: 1.004 s
│ └─Elapsed: 2.009 s
└─Elapsed: 3.010 s
```

## Features

### `ftimer.tracker()` 
Prints a text and the elapsed time in the same line. It is suggested for code sections that don't print any output.

  As a context:
```python
with ftimer.tracker("Inverting the matrix"):
  B = np.linalg.inv(A)
```
As a decorator:
```python
@ftimer.tracker("Inverting the matrix"):
def inv(A):
  return np.linalg.inv(A)
```
Will produce something like `Invering the matrix ... took 0.123 s`.

### `ftimer.section(text)`
It's useful when timing complex code with nested calls to other timed functions.

As a decorator:
```python
@ftimer.flat("f()"):
def inv(A):
  return np.linalg.inv(A)
```
As a context:
```python
@ftimer.section("Parsing")
def parse(file_name):
    flog.log("File name:", file_name)
    return None

@ftimer.section("Counting words")
def count_words(d):
    return 0

@ftimer.section("main")
def main():
    d = parse("words.txt")
    n = count_words(d)
    flog.log(n)
```
Will produce something like
```
┌─main
│ ┌─Parsing file
│ │ File name: words.txt
│ └─Elapsed: 1.234 s
│ ┌─Counting words
│ └─Elapsed: 5.678 s
└─Elapsed: 6.912 s
```

### `ftimer.flat()`
It's useful when timing code that prints text and we want the output to be flat (no indentation).

As a decorator:
```python
@ftimer.flat("Matrix inversion"):
def inv(A):
  return np.linalg.inv(A)
```
 As a context:
```python
with ftimer.flat("Matrix inversion"):
  B = np.linalg.inv(A)
```
Will produce something like
```
[*] Running: Matrix inversion
[*] Matrix inversion: took 0.123 s
```



