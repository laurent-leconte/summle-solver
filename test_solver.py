import pytest

import summle_v1 as v1
import summle_v2 as v2
import summle_v3 as v3


@pytest.fixture(scope="session")
def base_solutions():
    numbers = [v1.Solution(i) for i in range(1, 5)]
    solutions = v1.generate_solutions(numbers)
    return solutions


@pytest.fixture(scope="session")
def v2_solutions():
    numbers = [v2.Solution(i) for i in range(1, 5)]
    solutions = v2.generate_solutions(numbers)
    return solutions


@pytest.fixture(scope="session")
def v3_solutions():
    numbers = [v3.Solution(i) for i in range(1, 5)]
    solutions = v3.generate_solutions(numbers)
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
    assert v1.best_solution(base_solutions[1]).num_steps == 1


def test_solutions_for_11(base_solutions):
    assert len(base_solutions[11]) == 9
    assert v1.best_solution(base_solutions[11]).num_steps == 2
