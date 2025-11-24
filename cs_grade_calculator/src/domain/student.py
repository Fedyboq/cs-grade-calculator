from typing import List
from .evaluation import Evaluation

class Student:
    """
    Represents a student and their academic record.
    RF01, RNF01: Manages evaluations with a limit of 10.
    RF02: Tracks attendance status.
    """
    MAX_EVALUATIONS = 10

    def __init__(self, student_id: str):
        self.id = student_id
        self.evaluations: List[Evaluation] = []
        self.has_reached_min_classes: bool = False

    def add_evaluation(self, evaluation: Evaluation):
        if len(self.evaluations) >= self.MAX_EVALUATIONS:
            raise ValueError(f"Cannot add more than {self.MAX_EVALUATIONS} evaluations.")
        self.evaluations.append(evaluation)

    def set_attendance(self, has_reached_min: bool):
        self.has_reached_min_classes = has_reached_min
