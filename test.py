from servicios.parser_ecuaciones import convertir_texto_a_matrices
from metodo.metodo import gauss_seidel

# 1. Escribir ecuaciones directas como texto
ecuaciones = """
3x + 0y + z = 5
2x + 3y + 0z = 4
0x + y + 4z = 6
"""

# 2. Crear vector inicial, tolerancia y máximo de iteraciones
x_ini = [0, 0, 0]
tol = 0.0001
max_iter = 50

# 3. Convertir ecuaciones a matrices
A, b, variables = convertir_texto_a_matrices(ecuaciones)

# 4. Ejecutar Gauss-Seidel directamente
solucion, tabla = gauss_seidel(A, b, max_iter, tol, x_ini)

# 5. Mostrar resultados
print("Variables:", variables)
print("Solucion encontrada:", solucion)

print("\nTabla de iteraciones:")
for fila in tabla:
    print(fila)
