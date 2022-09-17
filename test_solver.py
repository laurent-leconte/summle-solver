import pytest

from summle import Solution, generate_solutions

@pytest.fixture
def numbers():
    return [Solution(i) for i in range(1, 5)]


def test_generate_solutions(numbers):
    generated = generate_solutions(numbers)
    for i in range(1, 28):
        assert i in generated
    assert 29 not in generated
    assert 36 in generated
    assert len(generated[36]) == 3
    assert generated[28].pop() == '(((3 * 2) + 1) * 4)'