from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from operator import add, floordiv, mul, sub
from typing import Any, Callable, Optional

from algos.base import BaseSolver

"""
Define a tree-like type for formulas. In pseudo-Ocaml :
type Formula = 
| Leaf of int
| Node of Solution * str * Solution
"""
Formula = int | tuple["Formula", str, "Formula"]


def eval_formula(formula: Formula) -> int:
    match formula:
        case int():
            return formula
        case (left, op, right):
            left_value = eval_formula(left)
            right_value = eval_formula(right)
            match op:
                case "+":
                    return left_value + right_value
                case "-":
                    return left_value - right_value
                case "*":
                    return left_value * right_value
                case "/":
                    return left_value // right_value
                case _:
                    raise ValueError(f"Unknown operator {op}")


def explain_formula(formula: Formula) -> list[str]:
    # Super inefficient - we re-eval each child every time we visit a node
    result = []
    match formula:
        case int():
            # print(f'{self.value} is an input')
            return result
        case (left, op, right):
            result.extend(explain_formula(left))
            result.extend(explain_formula(right))
            left_value = eval_formula(left)
            right_value = eval_formula(right)
            result.append(f"{left_value} {op} {right_value} = {eval_formula(formula)}")
            return result


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

    def explain(self, header: bool = True) -> list[str]:
        result = []
        if header:
            result.append(f"{self.value} can be computed in {self.num_steps} steps:")
        result.extend(explain_formula(self.formula))
        return result


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
                        solution = Solution(
                            value, left.formula, right.formula, op.symbol
                        )
                        solutions[value].add(solution)
                        if n > 2:
                            # if we still have at least 1 element in the original array,
                            # add the new value to a copy and append it to the queue
                            copy_of_copy = copy.copy()
                            copy_of_copy.append(solution)
                            fifo.append(copy_of_copy)
        return solutions
