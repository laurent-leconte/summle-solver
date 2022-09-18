import pytest

from summle import Solution, generate_solutions, best_solution


@pytest.fixture(scope="session")
def solutions():
    numbers = [Solution(i) for i in range(1, 5)]
    return generate_solutions(numbers)


def test_solutions_are_complete(solutions):
    for i in range(1, 28):
        assert i in solutions
    assert 29 not in solutions
    assert 36 in solutions
    assert len(solutions[36]) == 3


def test_solution_for_28(solutions):
    assert str(solutions[28].pop()) == "(((3, *, 2), +, 1), *, 4)"


def test_best_solution(solutions):
    assert best_solution(solutions[1]).num_steps == 1
