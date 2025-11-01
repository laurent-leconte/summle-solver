import pytest

import summle
from algos.v1 import Solver as V1
from algos.v2 import Solver as V2
from algos.v3 import Solver as V3


@pytest.fixture(scope="session")
def base_solutions():
    solver = V1([1, 2, 3, 4])
    solutions = solver.generate_solutions()
    return solutions


@pytest.fixture(scope="session")
def v2_solutions():
    solver = V2([1, 2, 3, 4])
    solutions = solver.generate_solutions()
    return solutions


@pytest.fixture(scope="session")
def v3_solutions():
    solver = V3([1, 2, 3, 4])
    solutions = solver.generate_solutions()
    return solutions


@pytest.fixture(scope="session")
def all_solutions(base_solutions, v2_solutions, v3_solutions):
    return [base_solutions, v2_solutions, v3_solutions]


def test_solutions_are_complete(all_solutions):
    for solutions in all_solutions:
        total_solutions = sum([len(s) for s in solutions.values()])
        assert total_solutions == 396
        for i in range(1, 28):
            assert i in solutions
        assert 29 not in solutions
        assert 36 in solutions
        assert len(solutions[36]) == 3


def test_solution_for_28(all_solutions):
    for solutions in all_solutions:
        assert str(solutions[28].pop()) in [
            "(((3, *, 2), +, 1), *, 4)",
            "(((3, '*', 2), '+', 1), *, 4)",
        ]


def test_best_solution(base_solutions):
    assert summle.best_solution(base_solutions[1]).num_steps == 1


def test_solutions_for_11(base_solutions):
    assert len(base_solutions[11]) == 9
    assert summle.best_solution(base_solutions[11]).num_steps == 2
