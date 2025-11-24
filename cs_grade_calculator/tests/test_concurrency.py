import threading
import time
import sys
import os
import random

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.domain.student import Student
from src.domain.evaluation import Evaluation
from src.services.calculator import GradeCalculator

def simulate_user_request(user_id, results, errors):
    try:
        # Setup data
        student = Student(f"User_{user_id}")
        # Randomize slightly to simulate real usage
        score1 = random.uniform(10, 20)
        score2 = random.uniform(5, 15)
        student.add_evaluation(Evaluation("Exam 1", score1, 50.0))
        student.add_evaluation(Evaluation("Exam 2", score2, 50.0))
        student.set_attendance(True)
        
        # Calculate
        start_time = time.time()
        calculator = GradeCalculator()
        result = calculator.calculate_final_grade(student, teachers_consensus=False)
        end_time = time.time()
        
        # Verify correctness (simple check)
        expected_avg = (score1 * 50 + score2 * 50) / 100
        if abs(result.weighted_average - expected_avg) > 0.01:
            raise ValueError("Calculation mismatch")
            
        duration = (end_time - start_time) * 1000 # ms
        results.append(duration)
        
    except Exception as e:
        errors.append(e)

def test_concurrency():
    print("=== Iniciando Prueba de Concurrencia (RNF02) ===")
    NUM_USERS = 50
    threads = []
    results = [] # Store execution times
    errors = []
    
    start_total = time.time()
    
    # Launch 50 threads
    for i in range(NUM_USERS):
        t = threading.Thread(target=simulate_user_request, args=(i, results, errors))
        threads.append(t)
        t.start()
        
    # Wait for all to finish
    for t in threads:
        t.join()
        
    end_total = time.time()
    total_duration = end_total - start_total
    
    print(f"\nResultados:")
    print(f"Usuarios simulados: {NUM_USERS}")
    print(f"Errores: {len(errors)}")
    if errors:
        print(f"Primer error: {errors[0]}")
        
    avg_time = sum(results) / len(results) if results else 0
    max_time = max(results) if results else 0
    
    print(f"Tiempo promedio por solicitud: {avg_time:.2f} ms")
    print(f"Tiempo máximo por solicitud: {max_time:.2f} ms")
    print(f"Tiempo total de la prueba: {total_duration:.2f} s")
    
    # Verification against RNF04 (< 300ms)
    if max_time < 300:
        print("\n[EXITO] RNF04 Cumplido: Todas las solicitudes < 300ms")
    else:
        print("\n[FALLO] RNF04 No Cumplido: Algunas solicitudes excedieron 300ms")

    if len(errors) == 0:
        print("[EXITO] RNF02 Cumplido: 50 usuarios concurrentes procesados sin errores.")
    else:
        print("[FALLO] RNF02 No Cumplido: Hubo errores durante la ejecución concurrente.")

if __name__ == "__main__":
    test_concurrency()
