import numpy as np
import pandas as pd

def gauss_seidel(A, b, max_iter, tol, x_ini):
    A = np.array(A, float)
    b = np.array(b, float).flatten()
    x = np.array(x_ini, float)

    n = len(b)
    datos = []

    for k in range(1, max_iter + 1):
        x_old = x.copy()

        for i in range(n):
            suma = sum(A[i,j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i,i]

        errores = np.abs((x - x_old) / np.where(x != 0, x, 1)) * 100
        datos.append([k] + list(x) + list(errores))

        if np.all(errores < tol * 100):
            break

    columnas = ["Iteracion"] + [f"x{i+1}" for i in range(n)] + [f"Error_x{i+1}" for i in range(n)]
    tabla = pd.DataFrame(datos, columns=columnas)

    return x, tabla
