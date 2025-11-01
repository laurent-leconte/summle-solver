import cProfile
import gc
import pstats
from random import shuffle
from time import perf_counter
from typing import Callable, List, Tuple

from algos import v1 as summle_v1
from algos import v2 as summle_v2
from algos import v3 as summle_v3

REFERENCE_INPUT = [2, 3, 6, 7, 10, 75]
REFERENCE_NUM_SOLUTIONS = 405677


def v1():
    solutions = summle_v1.generate_solutions(
        [summle_v1.Solution(i) for i in REFERENCE_INPUT]
    )
    return solutions


def v2():
    solutions = summle_v2.generate_solutions(
        [summle_v2.Solution(i) for i in REFERENCE_INPUT]
    )
    return solutions


def v3():
    solutions = summle_v3.generate_solutions(
        [summle_v3.Solution(i) for i in REFERENCE_INPUT]
    )
    return solutions


def measure_call(call: Callable, num_runs: int = 10) -> Tuple[float, float]:
    """Measure performance with GC disabled. Returns the average and best results over `num_runs` runs.

    Results are deleted after each run to limit the impact of memory consumption.
    """
    results = []
    for i in range(num_runs):
        gc.disable()
        start = perf_counter()
        solutions = call()
        duration = perf_counter() - start
        results.append(duration)
        sum_solutions = sum([len(s) for s in solutions.values()])
        assert sum_solutions == REFERENCE_NUM_SOLUTIONS
        gc.enable()
        del solutions
        print(f"Run {i} took {duration}s")
    return min(results), sum(results) / num_runs


def profile_call(call: Callable):
    with cProfile.Profile() as pr:
        call()
    stats = pstats.Stats(pr)
    clean_stats = stats.strip_dirs().sort_stats("tottime")
    clean_stats.print_stats()
    clean_stats.dump_stats(f"{call.__name__}_perf.prof")


def time(callables: List[Callable], num_rounds: int = 10) -> None:
    shuffle(callables)
    for c in callables:
        print(f"**** {c.__name__} ****")
        print(measure_call(c, num_rounds))


if __name__ == "__main__":
    time([v1, v2, v3])
    # profile_call(v3)
