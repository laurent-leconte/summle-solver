import argparse
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from operator import add, floordiv, mul, sub
from typing import Callable, List, Set, Optional, Tuple, Union, Iterable, Any


"""
Define a tree-like type for formulas. In pseudo-Ocaml :
type Formula = 
| Leaf of int
| Node of Solution * str * Solution
"""
Formula = Union[int, Tuple["Formula", str, "Formula"]]


class Solution:
    value: int
    formula: Formula

    def __init__(
        self,
        value: int,
        left: Optional[Formula] = None,
        right: Optional[Formula] = None,
        op: Optional[str] = None,
    ):
        self.value = value
        if left is not None:
            self.formula = (left, op, right)
        else:
            self.formula = value

    def __hash__(self) -> int:
        return hash(self.formula)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Solution):
            return False
        return self.formula == other.formula

    def __str__(self) -> str:
        if isinstance(self.formula, int):
            return str(self.value)
        else:
            left, op, right = self.formula
            return f"({left}, {op}, {right})"

    @property
    def num_steps(self):
        def formula_depth(formula: Formula):
            if isinstance(formula, int):
                return 0
            else:
                left, _, right = formula
                return 1 + formula_depth(left) + formula_depth(right)

        return formula_depth(self.formula)


@dataclass
class Operator:
    symbol: str
    op: Callable[[int, int], int]
    precondition: Callable[[int, int], bool]


operators = [
    Operator("+", add, lambda x, y: True),
    Operator("*", mul, lambda _, y: y > 1),  # only multiply numbers > 1
    Operator("-", sub, lambda x, y: x != y),  # only substract different numbers
    Operator(
        "/", floordiv, lambda x, y: y > 1 and x % y == 0
    ),  # divisor should be greater than 1 and evenly divide x
]


def generate_solutions(numbers: List[Solution]) -> dict[int, Set[Solution]]:
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
            right = copy.pop(j)
            left = copy.pop(i)
            # ensure left >= right
            if left.value < right.value:
                right, left = left, right

            for op in operators:
                if op.precondition(left.value, right.value):
                    value = op.op(left.value, right.value)
                    solution = Solution(value, left.formula, right.formula, op.symbol)
                    solutions[value].add(solution)
                    if n > 2:
                        # if we still have at least 1 element in the original array,
                        # add the new value to a copy and append it to the queue
                        copy_of_copy = copy.copy()
                        copy_of_copy.append(solution)
                        fifo.append(copy_of_copy)
    return solutions


def best_solution(solutions: Iterable[Solution]) -> Solution:
    return sorted(solutions, key=(lambda s: s.num_steps))[0]


def explain(s: Solution, header: bool = True) -> None:
    if header:
        print(f"{s.value} can be computed in {s.num_steps} steps:")
    if isinstance(s.formula, int):
        # print(f'{s.value} is an input')
        return
    else:
        left, op, right = s.formula
        explain(left, False)
        explain(right, False)
        print(f"{left.value} {op} {right.value} = {s.value}")


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
    target = args.target[0]
    if not target in solutions:
        print(f"Could not find a solution for {target}")
    else:
        explain(best_solution(solutions[target]))
