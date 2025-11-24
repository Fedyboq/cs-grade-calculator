from dataclasses import dataclass
from typing import List
from ..domain.student import Student
from .policies import AttendancePolicy, ExtraPointsPolicy

@dataclass
class CalculationResult:
    final_grade: float
    weighted_average: float
    attendance_penalty_applied: bool
    extra_points_applied: float

class GradeCalculator:
    """
    RF04, RF05: Calculates final grade and provides details.
    RNF03: Deterministic calculation.
    """
    MAX_GRADE = 20.0

    def calculate_final_grade(self, student: Student, teachers_consensus: bool) -> CalculationResult:
        # 1. Calculate Weighted Average
        total_weight = sum(e.weight for e in student.evaluations)
        if total_weight == 0:
            weighted_average = 0.0
        else:
            # Normalize weights if they don't sum to 100? 
            # Requirement says "percentage of weight". Assuming they should sum to 100 or be treated as relative.
            # Let's assume standard weighted average: sum(score * weight) / sum(weight)
            weighted_sum = sum(e.score * e.weight for e in student.evaluations)
            weighted_average = weighted_sum / total_weight

        # 2. Apply Attendance Penalty
        grade_after_attendance = AttendancePolicy.apply_penalty(weighted_average, student.has_reached_min_classes)
        penalty_applied = not student.has_reached_min_classes

        # 3. Apply Extra Points
        extra_points = ExtraPointsPolicy.calculate_bonus(teachers_consensus)
        final_grade = grade_after_attendance + extra_points

        # 4. Cap at Max Grade
        final_grade = min(final_grade, self.MAX_GRADE)
        
        # Ensure non-negative
        final_grade = max(0.0, final_grade)

        return CalculationResult(
            final_grade=round(final_grade, 2),
            weighted_average=round(weighted_average, 2),
            attendance_penalty_applied=penalty_applied,
            extra_points_applied=extra_points
        )
