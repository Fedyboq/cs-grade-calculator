import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.domain.student import Student
from src.domain.evaluation import Evaluation
from src.services.calculator import GradeCalculator

class TestGradeCalculator:
    
    def setup_method(self):
        self.calculator = GradeCalculator()
        self.student = Student("TEST001")

    def test_calculate_normal_case(self):
        """Test standard calculation with attendance and no extra points."""
        self.student.add_evaluation(Evaluation("Exam 1", 15.0, 50.0))
        self.student.add_evaluation(Evaluation("Exam 2", 17.0, 50.0))
        self.student.set_attendance(True)
        
        result = self.calculator.calculate_final_grade(self.student, teachers_consensus=False)
        
        # Avg: (15*50 + 17*50) / 100 = 16.0
        assert result.weighted_average == 16.0
        assert result.final_grade == 16.0
        assert not result.attendance_penalty_applied
        assert result.extra_points_applied == 0.0

    def test_attendance_penalty(self):
        """Test penalty application when attendance is not met."""
        self.student.add_evaluation(Evaluation("Exam 1", 20.0, 100.0))
        self.student.set_attendance(False) # Penalty 30%
        
        result = self.calculator.calculate_final_grade(self.student, teachers_consensus=False)
        
        # Avg: 20.0. Penalty: 20 * 0.7 = 14.0
        assert result.weighted_average == 20.0
        assert result.final_grade == 14.0
        assert result.attendance_penalty_applied

    def test_extra_points(self):
        """Test extra points addition."""
        self.student.add_evaluation(Evaluation("Exam 1", 15.0, 100.0))
        self.student.set_attendance(True)
        
        result = self.calculator.calculate_final_grade(self.student, teachers_consensus=True)
        
        # Avg: 15.0. Bonus: +1.0 = 16.0
        assert result.final_grade == 16.0
        assert result.extra_points_applied == 1.0

    def test_max_grade_cap(self):
        """Test that grade does not exceed 20.0."""
        self.student.add_evaluation(Evaluation("Exam 1", 20.0, 100.0))
        self.student.set_attendance(True)
        
        # 20 + 1 bonus = 21 -> should be 20
        result = self.calculator.calculate_final_grade(self.student, teachers_consensus=True)
        
        assert result.final_grade == 20.0

    def test_max_evaluations_error(self):
        """RNF01: Test max 10 evaluations limit."""
        for i in range(10):
            self.student.add_evaluation(Evaluation(f"E{i}", 10.0, 10.0))
            
        with pytest.raises(ValueError, match="Cannot add more than 10 evaluations"):
            self.student.add_evaluation(Evaluation("Overflow", 10.0, 10.0))

    def test_invalid_evaluation_values(self):
        """Test validation for scores and weights."""
        with pytest.raises(ValueError):
            Evaluation("Bad Score", -1.0, 50.0)
        with pytest.raises(ValueError):
            Evaluation("Bad Weight", 10.0, 101.0)

    def test_determinism(self):
        """RNF03: Test determinism."""
        self.student.add_evaluation(Evaluation("Exam 1", 12.34, 50.0))
        self.student.add_evaluation(Evaluation("Exam 2", 18.99, 50.0))
        self.student.set_attendance(True)
        
        result1 = self.calculator.calculate_final_grade(self.student, False)
        result2 = self.calculator.calculate_final_grade(self.student, False)
        
        assert result1.final_grade == result2.final_grade
