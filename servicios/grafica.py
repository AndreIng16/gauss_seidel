import matplotlib.pyplot as plt

def graficar_errores(tabla):
    columnas_error = [c for c in tabla.columns if "Error" in c]
    tabla["Error_promedio"] = tabla[columnas_error].mean(axis=1)

    plt.plot(tabla["Iteración"], tabla["Error_promedio"], marker="o")
    plt.title("Convergencia Gauss-Seidel")
    plt.xlabel("Iteración")
    plt.ylabel("Error promedio (%)")
    plt.grid(True)
    plt.show()
