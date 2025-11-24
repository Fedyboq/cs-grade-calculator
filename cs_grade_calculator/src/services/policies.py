class AttendancePolicy:
    """
    RF02: Handles attendance rules.
    """
    PENALTY_PERCENTAGE = 0.30  # 30% reduction if attendance not met

    @staticmethod
    def apply_penalty(grade: float, has_min_attendance: bool) -> float:
        if has_min_attendance:
            return grade
        return grade * (1 - AttendancePolicy.PENALTY_PERCENTAGE)

class ExtraPointsPolicy:
    """
    RF03: Handles extra points logic.
    """
    BONUS_POINTS = 1.0

    @staticmethod
    def calculate_bonus(teachers_consensus: bool) -> float:
        return ExtraPointsPolicy.BONUS_POINTS if teachers_consensus else 0.0
