from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from operator import add, floordiv, mul, sub
from typing import Callable, Optional, Iterable, Any
from algos.base import BaseSolution, BaseSolver

"""
Define a tree-like type for formulas. In pseudo-Ocaml :
type Formula = 
| Leaf of int
| Node of Solution * str * Solution
"""
Formula = int | tuple["Solution", str, "Solution"]


class Solution(BaseSolution):
    value: int
    str_formula: str
    formula: Formula
    num_steps: int

    def __init__(
        self,
        value: int,
        left: Optional["Solution"] = None,
        right: Optional["Solution"] = None,
        op: Optional[str] = None,
    ):
        self.value = value
        if left is None or right is None or op is None:
            self.formula = value
            self.num_steps = 0
            self.str_formula = str(value)
        else:
            self.formula = (left, op, right)
            self.num_steps = 1 + left.num_steps + right.num_steps
            self.str_formula = f"({left.str_formula}{op}{right.str_formula})"

    def __hash__(self) -> int:
        return hash(self.str_formula)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Solution):
            return False
        return self.str_formula == other.str_formula

    def __str__(self) -> str:
        if isinstance(self.formula, int):
            return str(self.value)
        else:
            left, op, right = self.formula
            return f"({left}, {op}, {right})"

    def explain(self, header: bool = True) -> list[str]:
        result = []
        if header:
            result.append(f"{self.value} can be computed in {self.num_steps} steps")

        match self.formula:
            case int():
                return result
            case (left, op, right):
                left_explain = left.explain(False)
                right_explain = right.explain(False)
                result.extend(left_explain)
                result.extend(right_explain)
                result.append(f"{left.value} {op} {right.value} = {self.value}")
                return result

    def used_numbers(self) -> list[int]:
        if isinstance(self.formula, int):
            return [self.value]
        else:
            left, _, right = self.formula
            return left.used_numbers() + right.used_numbers()


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


class Solver(BaseSolver):
    def __init__(self, inputs: list[int]):
        self.numbers = [Solution(i) for i in inputs]

    def generate_solutions(self) -> dict[int, set[Solution]]:
        fifo = deque([self.numbers])
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
                        solution = Solution(value, left, right, op.symbol)
                        solutions[value].add(solution)
                        if n > 2:
                            # if we still have at least 1 element in the original array,
                            # add the new value to a copy and append it to the queue
                            copy_of_copy = copy.copy()
                            copy_of_copy.append(solution)
                            fifo.append(copy_of_copy)
        return solutions
