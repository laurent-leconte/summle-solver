# summle-solver

This is a simple script to find solutions to [Summle challenges](https://summle.net/).

## Usage

```
python summle.py <target number> <list of input numbers>
```

## TODO

[X] add unit tests
[X] Make output easier to read
[X] (longer term) represent formulas as binary trees (rather than strings)
[ ] de-duplicate similar solutions e.g. (10 + 2) + 3 vs 10 + (3 + 2) vs (10 + 3) + 2
[ ] improve performance

## Performance tests

- Base `generate_solutions` method with [2, 3, 6, 7, 10, 75]: 4.484 secs (avg of 10 runs)
