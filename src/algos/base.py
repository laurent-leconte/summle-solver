from abc import ABC


class BaseSolution(ABC):
    def explain(self, header: bool = True) -> list[str]: ...

    def used_numbers(self) -> list[int]: ...

class BaseSolver(ABC):
    def generate_solutions(
        self, inputs: list[BaseSolution]
    ) -> dict[int, set[BaseSolution]]: ...
