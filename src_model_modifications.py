#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# ARCHIVO: src_model_modifications.py
# DESCRIPCIÓN: Código EXACTO que debe insertarse en la función compare_execution
#              del archivo src/model.py del proyecto original
# USO: Reemplazar SOLO la sección marcada con ##CODE FOR STUDENTS en src/model.py
# AUTOR: Claudia Maria Lopez Bombin Y Gonzalo Velasco Lucas
# FECHA: Noviembre 2025
# =============================================================================

import numpy as np
import time
from multiprocessing import Pool

# =============================================================================
# FUNCIÓN AUXILIAR: matrix_multiply
# =============================================================================
def matrix_multiply(size: int) -> float:
    """
    Realiza multiplicación de matrices cuadradas del tamaño especificado
    y devuelve el tiempo de ejecución.
    
    Esta función es utilizada internamente por compare_execution().
    
    Args:
        size (int): Tamaño de la matriz cuadrada (size x size)
        
    Returns:
        float: Tiempo en segundos que tomó la multiplicación
    """
    # Generar dos matrices aleatorias del tamaño especificado
    # Se usan números aleatorios para asegurar una carga de trabajo real
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    
    # Medir el tiempo exacto de la multiplicación
    start_time = time.time()
    result = np.dot(A, B)  # Multiplicación de matrices optimizada con NumPy
    end_time = time.time()
    
    # Devolver el tiempo transcurrido
    return end_time - start_time

# =============================================================================
# CÓDIGO EXACTO PARA INSERTAR EN src/model.py
# =============================================================================
"""
EN EL ARCHIVO src/model.py, BUSCAR ESTA FUNCIÓN:

def compare_execution() -> Tuple[float, float]:
    sequential_time = 0
    parallel_time = 0
    matrix_sizes = [310, 210, 400, 160]
    ##CODE FOR STUDENTS
    # END CODE FOR STUDENTS
    return sequential_time, parallel_time

Y REEMPLAZAR LA SECCIÓN ##CODE FOR STUDENTS CON ESTE CÓDIGO:
"""

# === INICIO DEL CÓDIGO A INSERTAR ===

    # EJECUCIÓN SECUENCIAL
    # =====================
    # Medir el tiempo total para procesar todas las matrices de forma secuencial
    # (una después de otra en el mismo proceso)
start_sequential = time.time()

# Procesar cada tamaño de matriz en secuencia
for size in matrix_sizes:
    # Llamar a matrix_multiply para cada tamaño
    # Esto se ejecuta en el mismo hilo/proceso
    matrix_multiply(size)

# Calcular el tiempo total secuencial
sequential_time = time.time() - start_sequential

# EJECUCIÓN PARALELA  
# ==================
# Medir el tiempo total para procesar matrices en paralelo
# usando 2 procesos (como especifica el enunciado)
start_parallel = time.time()

# Crear un pool de 2 procesos para ejecución paralela
# Pool permite distribuir el trabajo entre múltiples procesos
with Pool(processes=2) as pool:
    # pool.map distribuye las tareas entre los procesos disponibles
    # Cada proceso ejecuta matrix_multiply con un tamaño diferente
    # Esto permite que múltiples multiplicaciones se ejecuten simultáneamente
    pool.map(matrix_multiply, matrix_sizes)

# Calcular el tiempo total paralelo
parallel_time = time.time() - start_parallel

# === FIN DEL CÓDIGO A INSERTAR ===

"""
IMPORTANTE: También se debe agregar la función auxiliar matrix_multiply
en el mismo archivo src/model.py, fuera de la función compare_execution.
"""

# =============================================================================
# INSTRUCCIONES DETALLADAS DE IMPLEMENTACIÓN
# =============================================================================
"""
PASO A PASO PARA MODIFICAR src/model.py:

1. LOCALIZAR EL ARCHIVO:
   - Abrir: ProyectoFUSO/src/model.py

2. AGREGAR IMPORTS (si no existen):
   - Agregar al inicio del archivo, después de los otros imports:
     import numpy as np
     import time
     from multiprocessing import Pool

3. AGREGAR FUNCIÓN AUXILIAR matrix_multiply:
   - Buscar un lugar apropiado en el archivo (por ejemplo, después de las otras funciones)
   - Pegar la función matrix_multiply completa

4. MODIFICAR LA FUNCIÓN compare_execution:
   - Buscar la función compare_execution() en el archivo
   - Debe verse similar a esto:
        def compare_execution() -> Tuple[float, float]:
            sequential_time = 0
            parallel_time = 0
            matrix_sizes = [310, 210, 400, 160]
            ##CODE FOR STUDENTS
            # END CODE FOR STUDENTS
            return sequential_time, parallel_time

   - REEMPLAZAR desde ##CODE FOR STUDENTS hasta # END CODE FOR STUDENTS
     con el código proporcionado arriba

5. VERIFICAR LA ESTRUCTURA FINAL:
   - La función compare_execution debe quedar así:
        def compare_execution() -> Tuple[float, float]:
            sequential_time = 0
            parallel_time = 0
            matrix_sizes = [310, 210, 400, 160]
            
            # EJECUCIÓN SECUENCIAL
            start_sequential = time.time()
            for size in matrix_sizes:
                matrix_multiply(size)
            sequential_time = time.time() - start_sequential
            
            # EJECUCIÓN PARALELA
            start_parallel = time.time()
            with Pool(processes=2) as pool:
                pool.map(matrix_multiply, matrix_sizes)
            parallel_time = time.time() - start_parallel
            
            return sequential_time, parallel_time

6. GUARDAR Y PROBAR:
   - Guardar el archivo
   - Ejecutar el proyecto Flask
   - Navegar a http://localhost:5000/compare_execution
   - Verificar que muestre los tiempos de ejecución
"""

# =============================================================================
# EXPLICACIÓN DETALLADA DEL CÓDIGO
# =============================================================================
"""
¿QUÉ HACE ESTE CÓDIGO?

1. SECUENCIAL:
   - Ejecuta 4 multiplicaciones de matrices (310x310, 210x210, 400x400, 160x160)
   - Una DESPUÉS de la otra en el MISMO proceso
   - Mide el tiempo TOTAL de las 4 operaciones

2. PARALELO:
   - Ejecuta las mismas 4 multiplicaciones
   - Pero usa 2 procesos que trabajan SIMULTÁNEAMENTE
   - Un proceso puede hacer 310x310 mientras el otro hace 210x210
   - Luego continúan con las siguientes matrices
   - Mide el tiempo TOTAL de todas las operaciones

3. RESULTADO:
   - sequential_time: Tiempo total en modo secuencial
   - parallel_time: Tiempo total en modo paralelo
   - SpeedUp = sequential_time / parallel_time

¿POR QUÉ USAMOS Pool(processes=2)?
- El enunciado especifica "con 2 procesos maximizando el SpeedUp"
- 2 procesos es óptimo para 4 tareas (pueden distribuirse 2 y 2)
- Más procesos podrían generar overhead sin beneficio adicional

¿QUÉ SE ESPERA VER?
- En teoría: parallel_time < sequential_time (SpeedUp > 1)
- En la práctica: Depende del hardware, pero debería haber mejora
- La mejora no será 2x porque hay overhead de comunicación entre procesos
"""

def test_implementation():
    """
    Función de prueba para verificar que la implementación funciona correctamente.
    Puede ejecutarse independientemente para testing.
    """
    print("Probando implementación de compare_execution...")
    
    # Ejecutar la función modificada
    seq_time, par_time = compare_execution()
    
    print(f"Tiempo secuencial: {seq_time:.4f} segundos")
    print(f"Tiempo paralelo: {par_time:.4f} segundos")
    
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"SpeedUp: {speedup:.2f}x")
        print(f"Mejora: {((seq_time - par_time) / seq_time) * 100:.1f}%")
    
    return seq_time, par_time

if __name__ == "__main__":
    # Ejecutar prueba si el script se ejecuta directamente
    test_implementation()