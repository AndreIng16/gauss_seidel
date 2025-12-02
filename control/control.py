# -------------------------------------------------------------
# CONTROLADOR PRINCIPAL DEL SISTEMA GAUSS-SEIDEL
# -------------------------------------------------------------

from traduccion.parser_ecuaciones import convertir_texto_a_matrices
from metodo.metodo import gauss_seidel
from servicios.grafica import graficar_errores

class ControladorGaussSeidel:

    def __init__(self, vista):
        """
        Recibe una referencia a la interfaz gráfica (vista)
        para poder leer entradas y escribir resultados.
        """
        self.vista = vista

    # ---------------------------------------------------------
    # FUNCIÓN PRINCIPAL DEL CONTROLADOR
    # ---------------------------------------------------------
    def ejecutar(self):
        try:
            # 1. Leer datos desde la interfaz
            texto_ecuaciones = self.vista.obtener_ecuaciones()
            x_ini = self.vista.obtener_valores_iniciales()
            tol = self.vista.obtener_tolerancia()
            max_iter = self.vista.obtener_iteraciones()

            # 2. Convertir ecuaciones -> matrices
            A, b, variables = convertir_texto_a_matrices(texto_ecuaciones)

            # 3. Ejecutar el método
            solucion, tabla = gauss_seidel(A, b, max_iter, tol, x_ini)

            # 4. Mostrar tabla y solución final
            self.vista.mostrar_tabla(tabla)
            self.vista.mostrar_solucion(solucion, variables)

            # 5. Graficar
            graficar_errores(tabla)

        except Exception as e:
            self.vista.mostrar_error(f"Error: {str(e)}")

    # ---------------------------------------------------------
    # Función para limpiar pantalla
    # ---------------------------------------------------------
    def limpiar(self):
        self.vista.limpiar_campos()

    # ---------------------------------------------------------
    # Función para salir
    # ---------------------------------------------------------
    def salir(self):
        self.vista.cerrar_ventana()
