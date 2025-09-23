from typing import Iterable
import argparse
from algos.base import BaseSolution
from algos.v1 import Solver as V1Solver
from algos.v2 import Solver as V2Solver
from algos.v3 import Solver as V3Solver

algos = {"v1": V1Solver, "v2": V2Solver, "v3": V3Solver}


def best_solution(solutions: Iterable[BaseSolution]) -> BaseSolution:
    return sorted(solutions, key=(lambda s: s.num_steps))[0]


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
        print(f"There are {len(solutions[target])} solutions for {target}.")
        explain_best = best_solution(solutions[target]).explain(header=True)
        for line in explain_best:
            print(line)
