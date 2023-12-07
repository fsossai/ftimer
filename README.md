# Horatio :sunglasses:
Time your python scripts easily and with style. This tool uses [`fslog`](https://github.com/fsossai/fslog) to format its output.

The same classes can be used either through `with` or as a `@decorator`.

```
pip install horatio
```

## Example

```python
import horatio
import fslog
import time

@horatio.section("Factorial computation", tail="{0} took {1}")
def fact(n):
    if n == 1:
        fslog.log("Reached base case")
        return 1
    fslog.log("This is not the base case")
    with horatio.step("Sleeping for a second"):
        time.sleep(1)
    res = n * fact(n-1)
    return res

@horatio.section()
def main():
    fact(4)

main()
```
Will produce the following **output**:
```
┌─ main
│  ┌─ Factorial computation
│  │  This is not the base case
│  │  Sleeping for a second ... done in 1.005s
│  │  ┌─ Factorial computation
│  │  │  This is not the base case
│  │  │  Sleeping for a second ... done in 1.003s
│  │  │  ┌─ Factorial computation
│  │  │  │  This is not the base case
│  │  │  │  Sleeping for a second ... done in 1.004s
│  │  │  │  ┌─ Factorial computation
│  │  │  │  │  Reached base case
│  │  │  │  └─ Factorial computation took < 1 ms
│  │  │  └─ Factorial computation took 1.005s
│  │  └─ Factorial computation took 2.009s
│  └─ Factorial computation took 3.014s
└─ main: 3.015s
```

## Features

### `horatio.step()` 
Prints the description and the elapsed time in the same line. It is suggested for code sections that don't print any output.

  As a context:
```python
with horatio.step("Inverting the matrix"):
  B = np.linalg.inv(A)
```
As a decorator:
```python
@horatio.step("Inverting the matrix"):
def inv(A):
  return np.linalg.inv(A)
```
Will produce something like `Invering the matrix ... took 0.123 s`.

### `horatio.section()`
It's useful when timing complex code with nested calls to other timed functions.

As a decorator:
```python
@horatio.section():
def inv(A):
  return np.linalg.inv(A)
```
As a context:
```python
@horatio.section()
def parse(file_name):
    fslog.log("File name:", file_name)
    return None

@horatio.section()
def count_words(d):
    return 0

@horatio.section()
def main():
    d = parse("words.txt")
    n = count_words(d)
    fslog.log(n)
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

### `horatio.flat()`
It's useful when timing code that prints text and we want the output to be flat (no indentation).

As a decorator:
```python
@horatio.flat():
def inv(A):
  return np.linalg.inv(A)
```
 As a context:
```python
with horatio.flat("inv"):
  B = np.linalg.inv(A)
```
Will produce something like
```
[*] inv
[*] inv: 0.123 s
```



