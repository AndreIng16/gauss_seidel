import sympy as sp
import numpy as np

def convertir_texto_a_matrices(texto):
    ecuaciones = texto.split("\n")
    ecuaciones = [e for e in ecuaciones if e.strip()]

    exprs = [sp.sympify(eq.replace("=", "-(") + ")") for eq in ecuaciones]

    variables = sorted({str(s) for eq in exprs for s in eq.free_symbols})
    vars_sym = sp.symbols(variables)

    A, b = sp.linear_eq_to_matrix(exprs, vars_sym)

    return np.array(A, float), np.array(b, float), variables
