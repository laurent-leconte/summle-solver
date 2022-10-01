from time import perf_counter
from timeit import timeit
import gc
import cProfile
import pstats

from summle import generate_solutions, Solution

REFERENCE_INPUT = [2, 3, 6, 7, 10, 75]
REFERENCE_NUM_SOLUTIONS = 405677

def measure_base(num_runs = 10):
    """ Measure performance with GC disabled. Returns the average and best results over `num_runs` runs.
    
    Results are deleted after each run to limit the impact of memory consumption.
    """
    results = []
    for i in range(num_runs):
        gc.disable()
        start = perf_counter()
        solutions = generate_solutions([Solution(i) for i in REFERENCE_INPUT])
        duration = perf_counter() - start
        results.append(duration)
        sum_solutions = sum([len(s) for s in solutions.values()])
        assert sum_solutions == REFERENCE_NUM_SOLUTIONS
        gc.enable()
        del(solutions)
        print(f'Run {i} took {duration}s')
    return min(results), sum(results)/num_runs
    

def measure_base_timeit(num_runs = 10):
    res = timeit("generate_solutions([Solution(i) for i in REFERENCE_INPUT])", 
    setup="from summle import generate_solutions, Solution",
    globals=globals(),
    number=num_runs)
    return res / num_runs

# print("With timeit:", measure_base_timeit())
# print("Homegrown:", measure_base())

with cProfile.Profile() as pr:
    generate_solutions([Solution(i) for i in REFERENCE_INPUT])
stats = pstats.Stats(pr)
clean_stats = stats.strip_dirs().sort_stats("tottime")
clean_stats.print_stats()
clean_stats.dump_stats("base_perf.prof")