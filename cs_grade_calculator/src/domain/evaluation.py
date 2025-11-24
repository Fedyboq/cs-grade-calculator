from dataclasses import dataclass

@dataclass
class Evaluation:
    """
    Represents a single evaluation for a student.
    RF01: Stores score and weight.
    """
    name: str
    score: float
    weight: float

    def __post_init__(self):
        if not (0 <= self.score <= 20):
            raise ValueError("Score must be between 0 and 20.")
        if not (0 < self.weight <= 100):
            raise ValueError("Weight must be between 0 and 100.")
