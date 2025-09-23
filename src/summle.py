import argparse
import re

from typing import Iterable

from algos.base import BaseSolution
from algos.v1 import Solver as V1Solver
from algos.v2 import Solver as V2Solver
from algos.v3 import Solver as V3Solver

algos = {"v1": V1Solver, "v2": V2Solver, "v3": V3Solver}


def best_solution(solutions: Iterable[BaseSolution]) -> BaseSolution:
    return sorted(solutions, key=(lambda s: s.num_steps))[0]

def prime_factors(n: int) -> list[int]:
    """Return the prime factors of the given integer as a list of integers."""
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def evaluate_operation(input: str, previous: int=0) -> int | None:
    """
    Evaluate if a string is a valid arithmetic operation and return the result (None if not valid).
    A valid operation is of the form:
    [<left operand>] <operator> <right operand>
    where <left operand> and <right operand> are integers (the left operand is optional, and if missing, previous is used)
    and <operator> is one of +, -, *, /
    and the result is an integer (if left % right != 0 for division, return None)
    Examples:
    "3 + 4" -> 7
    "10 - 2" -> 8
    "* 2" (with previous=5) -> 10
    "/ 2" (with previous=10) -> 5
    "5 / 0" -> None (division by zero)
    "3 ^ 4" -> None (invalid operator)
    "hello" -> None (not a valid operation)
    """
    regex = r'^\s*(\d+)?\s*([\+\-\*\/])\s*(\d+)\s*$'
    match = re.match(regex, input)
    if not match:
        return None
    left, op, right = match.groups()
    left = int(left) if left is not None else previous
    right = int(right)
    
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        if right == 0 or left % right != 0:
            return None  # Division by zero or non-integer result
        return left // right
    return None

def run_interactive(solutions: list[BaseSolution], target: int, inputs: list[int]):
    print(f"There are {len(solutions)} solutions for {target}.")
    # Build hint list for best solution
    solution = best_solution(solutions)
    hints = solution.explain(header=True)
    num_steps = solution.num_steps
    if num_steps < len(inputs):
        new_hints = []
        unused_numbers = inputs.copy()
        for n in solution.used_numbers():
            unused_numbers.remove(n)
        for unused in unused_numbers:
            new_hints.append(f"{unused} is unused in this solution")
    # Add hints about unused numbers after the number of steps and before the detailed steps
    hints = hints[:1] + new_hints + hints[1:]

    previous = 0
    while True:
        user_input = input("Enter h for a hint, p for prime factors of target, all for all solutions, or a formula (q to quit): ")
        if user_input.lower() in ("q", "quit", "exit"):
            break
        elif user_input.lower() in ("all",):
            for sol in solutions:
                for line in sol.explain(header=True):
                    print(line)
                print("-" * 20)
        elif user_input.lower() in ("h", "hint"):
            if hints:
                print(hints.pop(0))
            else:
                print("No more hints available.")
        elif user_input.lower() in ("p", "prime", "factors"):
            factors = prime_factors(target)
            print(f"Prime factors of {target} are: {factors}")
        else:
            result = evaluate_operation(user_input, previous)
            if result is None:
                print("NaN")
            else:
                print(result)
                previous = result
                if result == target:
                    print("Congratulations! You've reached the target.")
                    break



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summle solver: given a target and a list of inputs, find all combinations of inputs that compute to the target value."
    )
    parser.add_argument(
        "-v",
        "--version",
        default="v2",
        choices=["v1", "v2", "v3"],
        help="the algorithm version to use (default: v2)",
    )
    parser.add_argument("-i", "--interactive", action="store_true", help="run in interactive mode")
    parser.add_argument("target", nargs=1, type=int, help="the target value to reach")
    parser.add_argument(
        "integers", nargs="+", type=int, help="the list of integer inputs"
    )
    args = parser.parse_args()
    solutions = algos[args.version](args.integers).generate_solutions()
    target = args.target[0]
    if not target in solutions:
        print(f"Could not find a solution for {target}")
    else:
        solutions_for_target = solutions[target]
        solution = best_solution(solutions_for_target)
        if args.interactive:
            run_interactive(solutions_for_target, target, args.integers)
        else:
            print(f"There are {len(solutions_for_target)} solutions for {target}.")
            explain_best = solution.explain(header=True)
            for line in explain_best:
                print(line)
