from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from estudiantes.models import Estudiante
from .models import RegistroNotas, DetalleNota



def dashboard(request):
    """Vista principal del dashboard de notas"""
    estudiantes = Estudiante.objects.all()

    registro = None
    notas = []

    estudiante_id = request.GET.get('estudiante')

    if estudiante_id:

        estudiante = Estudiante.objects.filter(
            id=estudiante_id
        ).first()

        if estudiante:

            registro, created = RegistroNotas.objects.get_or_create(
                estudiante=estudiante
            )

            notas = registro.detallenota_set.all()

        else:
            estudiante_id = None
            registro = None
            notas = []

    if request.method == "POST":
    
        # ==================================================
        # CRUD Estudiantes
        # ==================================================

        # CREAR ESTUDIANTE
        if 'guardar_estudiante' in request.POST:
            id_est = request.POST.get('id_estudiante', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            
            if not id_est or not nombre or not apellido:
                messages.error(request, 'Todos los campos son obligatorios')
            elif Estudiante.objects.filter(id_estudiante=id_est).exists():
                messages.error(request, f'La cédula {id_est} ya existe')
            else:
                try:
                    Estudiante.objects.create(
                        id_estudiante=id_est,
                        nombre=nombre,
                        apellido=apellido
                    )
                    messages.success(request, f'Estudiante {nombre} creado correctamente')
                except IntegrityError:
                    messages.error(request, 'Error al crear el estudiante')
            return redirect('/')

        # EDITAR ESTUDIANTE
        if 'editar_estudiante' in request.POST:
            estudiante = get_object_or_404(Estudiante, id=request.POST['id'])
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            
            if not nombre or not apellido:
                messages.error(request, 'Todos los campos son obligatorios')
            else:
                estudiante.nombre = nombre
                estudiante.apellido = apellido
                estudiante.save()
                messages.success(request, f'Estudiante {nombre} actualizado correctamente')
            return redirect('/')

        # ELIMINAR ESTUDIANTE
        if 'eliminar_estudiante' in request.POST:
            estudiante = get_object_or_404(Estudiante, id=request.POST['id'])
            nombre = estudiante.nombre
            estudiante.delete()
            messages.success(request, f'Estudiante {nombre} eliminado correctamente')
            return redirect('/')
        

        # ==================================================
        # CRUD NOTAS
        # ==================================================

        # CREAR NOTA
        if 'guardar_nota' in request.POST:
            estudiante_id = request.POST.get('estudiante_id')
            tipo = request.POST.get('tipo', '').strip()
            valor = request.POST.get('valor', '').strip()
            
            if not estudiante_id or not tipo or not valor:
                messages.error(request, 'Todos los campos son obligatorios')
                return redirect(f"/?estudiante={estudiante_id}")
            
            try:
                valor_float = float(valor)
                if valor_float < 0 or valor_float > 100:
                    messages.error(request, 'La nota debe estar entre 0 y 100')
                    return redirect(f"/?estudiante={estudiante_id}")
                    
                estudiante = get_object_or_404(Estudiante, id=estudiante_id)
                registro, _ = RegistroNotas.objects.get_or_create(estudiante=estudiante)
                
                DetalleNota.objects.create(
                    registro=registro,
                    tipo=tipo,
                    valor=valor_float
                )
                messages.success(request, f'Nota {tipo} agregada correctamente')
            except ValueError:
                messages.error(request, 'La nota debe ser un número válido')
            return redirect(f"/?estudiante={estudiante_id}")
        
           
        # EDITAR NOTA
        if 'editar_nota' in request.POST:
            nota_id = request.POST.get('nota_id')
            tipo = request.POST.get('tipo', '').strip()
            valor = request.POST.get('valor', '').strip()
            
            nota = get_object_or_404(DetalleNota, id=nota_id)
            est_id = nota.registro.estudiante.id
            
            if not tipo or not valor:
                messages.error(request, 'Todos los campos son obligatorios')
                return redirect(f"/?estudiante={est_id}")
            
            try:
                valor_float = float(valor)
                if valor_float < 0 or valor_float > 100:
                    messages.error(request, 'La nota debe estar entre 0 y 100')
                    return redirect(f"/?estudiante={est_id}")
                    
                nota.tipo = tipo
                nota.valor = valor_float
                nota.save()
                messages.success(request, f'Nota actualizada correctamente')
            except ValueError:
                messages.error(request, 'La nota debe ser un número válido')
            return redirect(f"/?estudiante={est_id}")

        # ELIMINAR NOTA
        if 'eliminar_nota' in request.POST:
            nota = get_object_or_404(DetalleNota, id=request.POST['nota_id'])
            est_id = nota.registro.estudiante.id
            tipo_nota = nota.tipo
            nota.delete()
            messages.success(request, f'Nota {tipo_nota} eliminada correctamente')
            return redirect(f"/?estudiante={est_id}")

    # Estudiante en edición (GET desde query param)
    estudiante_edit = None
    if request.GET.get('edit_id'):
        estudiante_edit = get_object_or_404(Estudiante, id=request.GET.get('edit_id'))
    
    # Nota en edición
    nota_edit = None
    if request.GET.get('edit_nota'):
        nota_edit = get_object_or_404(DetalleNota, id=request.GET.get('edit_nota'))
    
    return render(request, 'dashboard.html', {
        'estudiantes': estudiantes,
        'registro': registro,
        'notas': notas,
        'estudiante_edit': estudiante_edit,
        'nota_edit': nota_edit
    })

# Reportes
# REPORTE INDIVIDUAL
def reporte_individual(request):
    estudiante_id = request.GET.get('estudiante')

    registro = None
    notas = []

    if estudiante_id:
        registro = RegistroNotas.objects.filter(estudiante_id=estudiante_id).first()
        if registro:
            notas = registro.detallenota_set.all()

    return render(request, 'reportes/individual.html', {
        'registro': registro,
        'notas': notas
    })


# REPORTE GENERAL
def reporte_general(request):
    registros = RegistroNotas.objects.all()

    total = registros.count()
    aprobados = 0
    suma = 0

    for r in registros:
        prom = r.promedio()
        suma += prom
        if prom >= 60:
            aprobados += 1

    reprobados = total - aprobados
    promedio_general = round(suma / total, 2) if total > 0 else 0

    return render(request, 'reportes/general.html', {
        'registros': registros,
        'total': total,
        'aprobados': aprobados,
        'reprobados': reprobados,
        'promedio_general': promedio_general
    })