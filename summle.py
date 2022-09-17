import argparse
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from operator import add, ifloordiv, imul, sub
from typing import Callable, List, Set, Optional


class Solution:
    value: int
    formula: str

    def __init__(self, value: int, formula: Optional[str]=None):
        self.value = value
        self.formula = formula if formula is not None else str(value)

@dataclass
class Operator:
    symbol: str
    op: Callable[[int, int], int]
    precondition: Callable[[int, int], bool]


operators = [
    Operator("+", add, lambda x, y: True),
    Operator("*", imul, lambda _, y: y > 1),  # only multiply numbers > 1
    Operator("-", sub, lambda x, y: x != y),  # only substract different numbers
    Operator(
        "/", ifloordiv, lambda x, y: y > 1 and x % y == 0
    ),  # divisor should be greater than 1 and evenly divide x
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

            for op in operators:
                if op.precondition(op1.value, op2.value):
                    value = op.op(op1.value, op2.value)
                    formula = f"({op1.formula} {op.symbol} {op2.formula})"
                    solutions[value].add(formula)
                if n > 2:
                    # if we still have at least 1 element in the original array,
                    # add the new value to a copy and append it to the queue
                    copy_of_copy = copy.copy()
                    copy_of_copy.append(Solution(value, formula))
                    fifo.append(copy_of_copy)
    return solutions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summle solver: given a target and a list of inputs, find all combinations of inputs that compute to the target value."
    )
    parser.add_argument("target", nargs=1, type=int, help="the target value to reach")
    parser.add_argument(
        "integers", nargs="+", type=int, help="the list of integer inputs"
    )
    args = parser.parse_args()
    solutions = generate_solutions([Solution(i) for i in args.integers])
    print(solutions[args.target[0]])
