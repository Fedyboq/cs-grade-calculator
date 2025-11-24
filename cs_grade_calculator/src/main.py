import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.domain.student import Student
from src.domain.evaluation import Evaluation
from src.services.calculator import GradeCalculator

def main():
    print("=== CS-GradeCalculator ===")
    
    student_id = input("Ingrese el ID del estudiante: ")
    student = Student(student_id)

    # RF01: Register Evaluations
    print("\n--- Registro de Evaluaciones (Max 10) ---")
    while True:
        if len(student.evaluations) >= 10:
            print("Se ha alcanzado el número máximo de evaluaciones.")
            break
            
        choice = input("¿Desea agregar una evaluación? (s/n): ").lower()
        if choice != 's':
            break
            
        try:
            name = input("Nombre de la evaluación: ")
            score = float(input("Nota (0-20): "))
            weight = float(input("Peso (%): "))
            
            eval_obj = Evaluation(name, score, weight)
            student.add_evaluation(eval_obj)
            print("Evaluación agregada correctamente.")
        except ValueError as e:
            print(f"Error: {e}")

    # RF02: Attendance
    print("\n--- Registro de Asistencia ---")
    attendance_input = input("¿El estudiante cumplió con la asistencia mínima? (s/n): ").lower()
    student.set_attendance(attendance_input == 's')

    # RF03: Extra Points Policy
    print("\n--- Política de Puntos Extra ---")
    consensus_input = input("¿Existe consenso docente para puntos extra? (s/n): ").lower()
    teachers_consensus = (consensus_input == 's')

    # RF04: Calculate
    calculator = GradeCalculator()
    result = calculator.calculate_final_grade(student, teachers_consensus)

    # RF05: Display Details
    print("\n=== Detalle del Cálculo ===")
    print(f"Estudiante: {student.id}")
    print(f"Promedio Ponderado: {result.weighted_average}")
    print(f"Penalización por Asistencia Aplicada: {'SÍ' if result.attendance_penalty_applied else 'NO'}")
    print(f"Puntos Extra Aplicados: +{result.extra_points_applied}")
    print("---------------------------")
    print(f"NOTA FINAL: {result.final_grade}")

if __name__ == "__main__":
    main()
