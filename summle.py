import argparse
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from operator import add, sub, imul, ifloordiv
from typing import List, Set, Callable


@dataclass
class Solution:
    value: int
    formula: str

@dataclass
class Operator:
    symbol: str
    op: Callable[[int, int], int]
    precondition: Callable[[int, int], bool]


operators = [
    Operator('+', add, lambda x,y:True),
    Operator('-', sub, lambda x,y: x != y),  # only substract different numbers
    Operator('*', imul, lambda _,y: y > 1),  # only multiply numbers > 1
    Operator('/', ifloordiv, lambda x,y: y > 1 and x % y == 0),  # divisor should be greater than 1 and evenly divide x
]

def generate_solutions(numbers: List[Solution]) -> dict[int, Set[str]]:
    fifo = deque([numbers])
    solutions = defaultdict(set)
    while len(fifo) > 0:
        current = fifo.popleft()
        n = len(current)
        if n < 2:
            continue  # not enough numbers in the candidate to do anything

        # For all pairs of numbers in the candidate list, pop them and replace them
        # with the result of all possible operations between these numbers
        for i, j in combinations(range(n), 2):
            copy = current.copy()
            # pop j first to avoid off-by-one issues (j > i)
            op2 = copy.pop(j)
            op1 = copy.pop(i)
            # ensure op1 >= op2
            if op1.value < op2.value:
                op2, op1 = op1, op2
            added = Solution(op1.value + op2.value, f"({op1.formula} + {op2.formula})")
            solutions[added.value].add(added.formula)
            if n > 2:
                copy_added = copy.copy()
                copy_added.append(added)
                fifo.append(copy_added)
            # add multiplication if op2 is larger than 1
            if op2.value > 1:
                mult = Solution(
                    op1.value * op2.value, f"({op1.formula} * {op2.formula})"
                )
                solutions[mult.value].add(mult.formula)
                if n > 2:
                    copy_mult = copy.copy()
                    copy_mult.append(mult)
                    fifo.append(copy_mult)
            # add substraction if the values are different
            if op1.value != op2.value:
                sub = Solution(
                    op1.value - op2.value, f"({op1.formula} - {op2.formula})"
                )
                solutions[sub.value].add(sub.formula)
                if n > 2:
                    copy_sub = copy.copy()
                    copy_sub.append(sub)
                    fifo.append(copy_sub)
            # add division if op2 is not 0 or 1, and op1 is divisible by op2
            if op2.value > 1 and op1.value % op2.value == 0:
                divided = Solution(
                    op1.value // op2.value, f"({op1.formula} / {op2.formula})"
                )
                solutions[divided.value].add(divided.formula)
                if n > 2:
                    copy_divided = copy.copy()
                    copy_divided.append(divided)
                    fifo.append(copy_divided)
    return solutions


if __name__ == "__main__":
    numbers = [2, 3, 5, 6, 10, 10]
    target = 708
    solutions = generate_solutions([Solution(i, str(i)) for i in numbers])
    print(solutions[target])
