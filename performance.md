# Improving performance

## Base performances

With the reference input, the base algorithms runs in ~4.5 seconds on average, with a best run around 4.2 seconds.

| ncalls           | tottime | percall | cumtime | percall | filename:lineno(function)                         |
| ---------------- | ------- | ------- | ------- | ------- | ------------------------------------------------- |
| 1                | 2.785   | 2.785   | 11.913  | 11.913  | summle.py:71(generate_solutions)                  |
| 12357207/1247601 | 2.215   | 0.000   | 3.779   | 0.000   | {built-in method builtins.hash}                   |
| 12357207/1247601 | 1.780   | 0.000   | 3.995   | 0.000   | summle.py:34(**hash**)                            |
| 3290588/841924   | 1.684   | 0.000   | 2.068   | 0.000   | summle.py:37(**eq**)                              |
| 1571688          | 1.530   | 0.000   | 1.627   | 0.000   | summle.py:23(**init**)                            |
| 1247601          | 0.730   | 0.000   | 6.793   | 0.000   | {method 'add' of 'set' objects}                   |
| 8152858          | 0.481   | 0.000   | 0.481   | 0.000   | {built-in method builtins.isinstance}             |
| 1                | 0.247   | 0.247   | 12.160  | 12.160  | <string>:1(<module>)                              |
| 717575           | 0.126   | 0.000   | 0.126   | 0.000   | {method 'copy' of 'list' objects}                 |
| 786988           | 0.079   | 0.000   | 0.079   | 0.000   | {method 'pop' of 'list' objects}                  |
| 648165           | 0.076   | 0.000   | 0.076   | 0.000   | {built-in method builtins.len}                    |
| 393494           | 0.063   | 0.000   | 0.063   | 0.000   | summle.py:66(<lambda>)                            |
| 391163           | 0.046   | 0.000   | 0.046   | 0.000   | {built-in method \_operator.sub}                  |
| 393494           | 0.046   | 0.000   | 0.046   | 0.000   | {built-in method \_operator.add}                  |
| 379162           | 0.045   | 0.000   | 0.045   | 0.000   | {built-in method \_operator.mul}                  |
| 393494           | 0.045   | 0.000   | 0.045   | 0.000   | summle.py:63(<lambda>)                            |
| 324081           | 0.040   | 0.000   | 0.040   | 0.000   | {method 'append' of 'list' objects}               |
| 393494           | 0.040   | 0.000   | 0.040   | 0.000   | summle.py:64(<lambda>)                            |
| 393494           | 0.034   | 0.000   | 0.034   | 0.000   | summle.py:62(<lambda>)                            |
| 324082           | 0.033   | 0.000   | 0.033   | 0.000   | {method 'popleft' of 'collections.deque' objects} |
| 324081           | 0.025   | 0.000   | 0.025   | 0.000   | {method 'append' of 'collections.deque' objects}  |
| 83782            | 0.011   | 0.000   | 0.011   | 0.000   | {built-in method \_operator.floordiv}             |
| 1                | 0.000   | 0.000   | 12.160  | 12.160  | {built-in method builtins.exec}                   |
| 1                | 0.000   | 0.000   | 0.000   | 0.000   | <string>:1(<listcomp>)                            |
| 1                | 0.000   | 0.000   | 0.000   | 0.000   | {method 'disable' of '\_lsprof.Profiler' objects} |

![Flamegraph](base_perf.svg)
