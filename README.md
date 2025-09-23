# summle-solver

This is a simple script to find solutions to [Summle challenges](https://summle.net/).

## Usage

Solve a puzzle:

```
python src/summle.py <target number> <list of input numbers>
```

Interactive mode (shows hint, command-line calculator, prime decomposition):

```
python src/summle.py -i <target number> <list of input numbers>
```

## TODO

[X] add unit tests
[X] Make output easier to read
[X] (longer term) represent formulas as binary trees (rather than strings)
[ ] de-duplicate similar solutions e.g. (10 + 2) + 3 vs 10 + (3 + 2) vs (10 + 3) + 2
[ ] improve performance (delegate solution generation to the OCaml code?)
[X] add "hints" mode: decompose target, give a hint
[ ] download daily puzzle (make cli input an option)
[ ] refactor v2 solver as a subclass of v1 (only the hash functions differ)
