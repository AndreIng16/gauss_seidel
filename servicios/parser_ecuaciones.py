import sympy as sp
import numpy as np
import re

def convertir_texto_a_matrices(texto):
    ecuaciones = texto.split("\n")
    ecuaciones = [e.strip() for e in ecuaciones if e.strip()]

    ecuaciones_limpias = []

    for eq in ecuaciones:
        # Inserta multiplicación entre número y variable, ej: "3x" -> "3*x"
        eq = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", eq)

        # Maneja casos como "-3x"
        eq = re.sub(r"(\-)(\d)([a-zA-Z])", r"-\2*\3", eq)

        ecuaciones_limpias.append(eq)

    # Convertir ecuaciones tipo "3*x + 2*y = 5" → "3*x + 2*y -(5)"
    exprs = [sp.sympify(eq.replace("=", "-(") + ")") for eq in ecuaciones_limpias]

    # Obtener variables ordenadas
    variables = sorted({str(s) for eq in exprs for s in eq.free_symbols})
    vars_sym = sp.symbols(variables)

    A, b = sp.linear_eq_to_matrix(exprs, vars_sym)

    return np.array(A, float), np.array(b, float), variables
