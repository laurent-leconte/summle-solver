from abc import ABC, abstractmethod


class BaseSolution(ABC):
    @abstractmethod
    def explain(self, header: bool = True) -> list[str]: ...

    @abstractmethod
    def used_numbers(self) -> list[int]: ...


class BaseSolver(ABC):
    @abstractmethod
    def generate_solutions(
        self, inputs: list[BaseSolution]
    ) -> dict[int, set[BaseSolution]]: ...
