import argparse
import re
from typing import Iterable
from urllib.request import urlopen

from algos.base import BaseSolution
from algos.v1 import Solver as V1Solver
from algos.v2 import Solver as V2Solver
from algos.v3 import Solver as V3Solver

ALGOS = {"v1": V1Solver, "v2": V2Solver, "v3": V3Solver}
DIFFICULTIES = {"medium": "", "hard": "/hard", "extreme": "/extreme"}


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


def evaluate_operation(input: str, previous: int = 0) -> tuple[str, int | None]:
    """
    Evaluate if a string is a valid arithmetic operation and compute it if so.
    Returns a tuple of :
    - a string with either the result or "NaN" if the operation is invalid
    - the result as an integer or None if the operation is invalid or doesn't yield an integer result

    A valid operation is of the form:
    [<left operand>] <operator> [<right operand>]
    where <left operand> and <right operand> are integers
    (at least one operand must be supplied; if an operand is missing, previous is used)
    and <operator> is one of +, -, *, /, p
    (p means "prime factors ofoperand")
    Examples:
    "3 + 4" -> 7
    "10 - 2" -> 8
    "* 2" (with previous=5) -> 10
    "/ 2" (with previous=10) -> 5
    "p 15" -> [3, 5]
    "p" (with previous=28) -> [2, 2, 7]
    "5 / 0" -> None (division by zero)
    "3 ^ 4" -> None (invalid operator)
    "hello" -> None (not a valid operation)
    """
    regex = r"^\s*(\d+)?\s*([\+\-\*\/p])\s*(\d+)?\s*$"
    match = re.match(regex, input)
    if not match:
        return (f"Wrong format ({input})", None)
    left, op, right = match.groups()
    if left is None and right is None and op != "p":
        return ("No input", None)  # At least one operand must be supplied

    # unary operations : require one of left, right, previous
    if op == "p":
        operand = (
            int(left)
            if left is not None
            else (int(right) if right is not None else previous)
        )
        return (str(prime_factors(operand)), None)

    # At this point we know at least one of left, right has been supplied
    left = int(left) if left is not None else previous
    right = int(right) if right is not None else previous

    if op == "+":
        return (str(left + right), left + right)
    elif op == "-":
        return (str(left - right), left - right)
    elif op == "*":
        return (str(left * right), left * right)
    elif op == "/":
        if right == 0:
            return ("NaN", None)  # Division by zero
        result = left // right if left % right == 0 else left / right
        return (str(result), result if isinstance(result, int) else None)
    return ("NaN", None)


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
        user_input = input(
            "Enter h for a hint, p for prime factors of target, all for all solutions, or a formula (q to quit): "
        )
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
            str_result, newval = evaluate_operation(user_input, previous)
            print(str_result)
            if newval is not None:
                previous = newval
                if newval == target:
                    print("Congratulations! You've reached the target.")
                    break


def fetch_daily_problem(difficulty: str) -> tuple[int, list[int]]:
    """Fetch the daily problem for the given difficulty level from summle.net."""

    url = "https://summle.net" + DIFFICULTIES[difficulty]
    # window.puzzString contains the numbers and target as a comma-separated string
    puzzle_pattern = r'window\.puzzString\s*=\s*"([^"]+)";'

    with urlopen(url) as response:
        html = response.read().decode("utf-8")

    puzzle_match = re.search(puzzle_pattern, html)

    if puzzle_match:
        puzzle_string = puzzle_match.group(1)
        puzzle_numbers = list(map(int, puzzle_string.split(",")))
        target = puzzle_numbers[-1]
        numbers = puzzle_numbers[:-1]
        print(f"Fetched {difficulty} daily problem: target={target}, numbers={numbers}")
        return target, numbers

    raise ValueError("Could not find daily problem.")


def main():
    parser = argparse.ArgumentParser(
        description="Summle solver. Helper for the summle.net number game. Accepts either a target and a list of integers, or a difficulty level (easy, medium, hard).",
        epilog=(
            "Examples:\n"
            "  summle 831 100 3 7 9 25 50\n"
            "  summle -v v3 -i 562 2 3 7 8 10\n"
            "  summle hard\n"
            "  summle -i medium\n"
        ),
    )
    # Add common arguments
    parser.add_argument(
        "-v",
        "--version",
        default="v2",
        choices=["v1", "v2", "v3"],
        help="the algorithm version to use (default: v2)",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="run in interactive mode"
    )

    # Figure out if we have target + integers or difficulty
    known_args, rest = parser.parse_known_args()

    if not rest:
        parser.error("Provide either: TARGET INTEGERS...  or  DIFFICULTY")

    first = rest[0]
    if first.isdigit():
        # define parser for target + integers
        direct = argparse.ArgumentParser(add_help=False)
        direct.add_argument("target", type=int)
        direct.add_argument("integers", type=int, nargs="+")
        args = direct.parse_args(rest)
        target = args.target
        numbers = args.integers
    elif (difficulty := first.lower()) in DIFFICULTIES.keys():
        target, numbers = fetch_daily_problem(difficulty)
    else:
        parser.error(
            f"Unrecognized difficulty level: {first}. Valid levels are: {', '.join(DIFFICULTIES.keys())}"
        )

    algo = ALGOS[known_args.version]
    solutions = algo(numbers).generate_solutions()
    if target not in solutions:
        print(f"Could not find a solution for {target}")
    else:
        solutions_for_target = solutions[target]
        solution = best_solution(solutions_for_target)
        if known_args.interactive:
            run_interactive(solutions_for_target, target, numbers)
        else:
            print(f"There are {len(solutions_for_target)} solutions for {target}.")
            explain_best = solution.explain(header=True)
            for line in explain_best:
                print(line)


if __name__ == "__main__":
    main()
