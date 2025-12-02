from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
import numpy as np

from .models import SistemaEcuaciones, Solucion, Iteracion
from traduccion.parser_ecuaciones import convertir_texto_a_matrices
from metodo.metodo import gauss_seidel


def index(request):
    sistemas = SistemaEcuaciones.objects.all()[:10]
    return render(request, 'index.html', {'sistemas': sistemas})


def resolver(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', 'Sistema sin nombre')
            ecuaciones = request.POST.get('ecuaciones', '')
            valores_iniciales = request.POST.get('valores_iniciales', '0,0,0')
            tolerancia = float(request.POST.get('tolerancia', 0.0001))
            max_iter = int(request.POST.get('max_iteraciones', 50))
            
            x_ini = [float(x.strip()) for x in valores_iniciales.split(',')]
            
            A, b, variables = convertir_texto_a_matrices(ecuaciones)
            solucion, tabla = gauss_seidel(A, b, max_iter, tolerancia, x_ini)
            
            sistema = SistemaEcuaciones.objects.create(
                nombre=nombre,
                ecuaciones=ecuaciones,
                valores_iniciales=valores_iniciales,
                tolerancia=tolerancia,
                max_iteraciones=max_iter
            )
            
            Solucion.objects.create(
                sistema=sistema,
                solucion=json.dumps(solucion.tolist()),
                variables=json.dumps(variables),
                convergio=True,
                iteraciones_usadas=len(tabla)
            )
            
            for _, fila in tabla.iterrows():
                n_vars = len(variables)
                valores = fila[1:n_vars+1].tolist()
                errores = fila[n_vars+1:].tolist()
                
                Iteracion.objects.create(
                    sistema=sistema,
                    numero=int(fila['Iteracion']),
                    valores=json.dumps(valores),
                    errores=json.dumps(errores)
                )
            
            messages.success(request, f'Sistema resuelto en {len(tabla)} iteraciones')
            return redirect('resultado', sistema_id=sistema.id)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('index')


def resultado(request, sistema_id):
    sistema = get_object_or_404(SistemaEcuaciones, id=sistema_id)
    solucion = get_object_or_404(Solucion, sistema=sistema)
    iteraciones = sistema.iteraciones.all()
    
    sol_valores = json.loads(solucion.solucion)
    variables = json.loads(solucion.variables)
    
    tabla_datos = []
    for iteracion in iteraciones:
        valores = json.loads(iteracion.valores)
        errores = json.loads(iteracion.errores)
        tabla_datos.append({
            'numero': iteracion.numero,
            'valores': valores,
            'errores': errores
        })
    
    errores_promedio = []
    for iteracion in iteraciones:
        errores = json.loads(iteracion.errores)
        errores_promedio.append(sum(errores) / len(errores))
    
    
    pares = list(zip(variables, sol_valores))
    
    context = {
        'sistema': sistema,
        'solucion': solucion,
        'pares': pares,              # ← SE ENVÍA AL TEMPLATE
        'variables': variables,
        'tabla_datos': tabla_datos,
        'errores_promedio': json.dumps(errores_promedio),
        'iteraciones_nums': json.dumps(list(range(1, len(iteraciones) + 1)))
    }
    
    return render(request, 'resultado.html', context)


def historial(request):
    sistemas = SistemaEcuaciones.objects.all()
    return render(request, 'historial.html', {'sistemas': sistemas})


def eliminar_sistema(request, sistema_id):
    sistema = get_object_or_404(SistemaEcuaciones, id=sistema_id)
    sistema.delete()
    messages.success(request, 'Sistema eliminado')
    return redirect('historial')