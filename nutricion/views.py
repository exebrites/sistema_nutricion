import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from experto.main import evaluar_nutricion
from .models import Alimento, Dieta, DietaAlimento
from .forms import AlimentoForm


from django.core.paginator import Paginator
# home


def index(request):
    return render(request, "home.html")

# crud alimentos


def crear_alimento(request):
    if request.method == "POST":
        form = AlimentoForm(request.POST)

        if form.is_valid():
            alimento = form.save()

            return render(request, "alimentos/form.html", {
                "form": AlimentoForm(),
                "success": "Alimento creado correctamente.",
                "advertencias": form.advertencias,
                "info": form.info
            })
    else:
        form = AlimentoForm()

    return render(request, "alimentos/form.html", {"form": form})


def lista_alimentos(request):
    listado_completo = Alimento.objects.all().order_by('id')
    # ¡OJO! Siempre usa .order_by() al paginar para evitar resultados inconsistentes

    # 2. Configurar el Paginador
    # Paginator(objeto_a_paginar, cantidad_por_pagina)
    # Mostraremos 6 alimentos por página
    paginator = Paginator(listado_completo, 6)

    # 3. Obtener el número de página de la URL (?page=2)
    page_number = request.GET.get('page')

    # 4. Obtener el objeto de la página actual
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "alimentos/lista.html", context)


def editar_alimento(request, alimento_id):
    return HttpResponse("Editar alimento %s" % alimento_id)


def eliminar_alimento(request, alimento_id):
    return HttpResponse("Eliminar alimento %s" % alimento_id)


def alimento_detail(request, alimento_id):
    return HttpResponse("Detalle del alimento %s" % alimento_id)

# crud dieta


def lista_dietas(request):
    listado_completo = Dieta.objects.all().order_by('id')
    paginator = Paginator(listado_completo, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "dietas/lista.html", context)


def ver_dieta(request, dieta_id):
    dieta = Dieta.objects.get(id=dieta_id)
    alimentos_dieta = DietaAlimento.objects.filter(dieta=dieta)
    return render(request, "dietas/ver_dieta.html", {
        "dieta": dieta,
        "alimentos_dieta": alimentos_dieta
    })


def editar_dieta(request, dieta_id):
    return HttpResponse("Editar dieta %s" % dieta_id)


def eliminar_dieta(request, dieta_id):
    return HttpResponse("Eliminar dieta %s" % dieta_id)


def crear_dieta(request):
    carrito_dieta = request.session.get("carrito_dieta", [])
    resumen_dieta = request.session.get("datos_analisis_temporal", {})
    context = {
        "carrito_dieta": carrito_dieta,
        "resumen_dieta": resumen_dieta
    }
    if request.method == "POST":
        # validar lista de alimentos
        if not carrito_dieta:
            context["error"] = "La dieta debe contener al menos un alimento."
            return render(request, "dietas/form.html", context)
        # return HttpResponse(json.dumps(carrito_dieta[1]['id']))
        # obtneer todos los alimentos
        # crear una dieta
        # crear un detalle de dieta por cada alimento
        dieta = Dieta.objects.create(
            nombre=request.POST.get("nombre", "Dieta sin nombre"),
            descripcion=request.POST.get("descripcion", ""))
        for alimento_carrito in carrito_dieta:
            alimento = Alimento.objects.get(id=alimento_carrito["id"])
            DietaAlimento.objects.create(
                alimento=alimento,
                dieta=dieta,
                cantidad=alimento_carrito["cantidad"],
                unidad=alimento_carrito["unidad"],
            )
        request.session["carrito_dieta"] = []
        request.session["datos_analisis_temporal"] = {}
        return redirect('lista_dietas')
        # return HttpResponse("Dieta creada correctamente.")
        # limpiar la sesion
    return render(request, "dietas/form.html", context)


def alimentos_dieta(request):
    if request.method == "POST":
        alimento_id = request.POST.get("alimento")
        cantidad = float(request.POST.get("cantidad", 0))
        unidad = request.POST.get("unidad", "g")
        if alimento_id not in request.session.get("carrito_dieta", []):
            alimento = Alimento.objects.get(id=alimento_id)
            request.session["carrito_dieta"] = request.session.get("carrito_dieta", []) + [
                {
                    "id": alimento_id,
                    "nombre": alimento.nombre,
                    "calorias": alimento.calorias,
                    "cantidad": cantidad,
                    "unidad": unidad,
                }
            ]
            return redirect('create_dieta')
        else:
            return render(request, "dietas/listar_alimentos_dieta.html", {
                "error": f"El alimento {Alimento.objects.get(id=alimento_id).nombre} ya est  en la dieta",
                "alimentos": Alimento.objects.all()
            })

    return render(request, "dietas/listar_alimentos_dieta.html", {
        "alimentos": Alimento.objects.all()
    })


def vaciar_alimento_dieta(request):
    request.session["carrito_dieta"] = []
    return redirect('create_dieta')


def borrar_alimento_dieta(request, alimento_id):
    carrito_dieta = request.session.get("carrito_dieta", [])
    carrito_dieta = [a for a in carrito_dieta if a["id"] != str(alimento_id)]
    request.session["carrito_dieta"] = carrito_dieta
    return redirect('create_dieta')


def validar_alimentos(request):
    alimentos_dieta = request.session.get("carrito_dieta", [])
    context = {}
    # validar lista de alimentos
    if not alimentos_dieta:
        context["error"] = "La dieta debe contener al menos un alimento."
        return render(request, "dietas/form.html", context)

    resumen = {}
    for a in alimentos_dieta:
        alimento = Alimento.objects.get(id=a['id'])
        data = {
            "calorias": alimento.calorias,
            "proteinas": alimento.proteinas,
            "sodio": alimento.sodio,
            "carbohidratos": alimento.carbohidratos,
            "grasas": alimento.grasas,
        }
        response = evaluar_nutricion(data, modo="nutricion")

        resumen[alimento.id] = {
            'alimento': alimento.to_dict(),
            'evaluacion': response
        }

    # # 2. Guardamos en la sesión
    # request.session['datos_analisis_temporal'] = resultados_analisis

    # # 3. Redirigimos LIMPIAMENTE (sin argumentos en la URL)
    return render(request, "dietas/validar_alimentos.html", {
        "resumen": resumen})
# consulta


def primera_consulta(request):
    return render(request, "consultas/primera_consulta.html")


def crear_paciente(request):
    context = {}
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")
        # 1. Aquí puedes guardar los datos del paciente en la base de datos
        datos_paciente = {
            "nombre": nombre,
            "edad": edad,
            "sexo": sexo
        }

        context["datos_paciente"] = datos_paciente
        return render(request, "consultas/motivo_consulta.html", context)

    return HttpResponse("Método no permitido.", status=405)


def agregar_sintoma_motivo_consulta(request):
    # texto: "fatiga,dolor de cabeza,..."
    sintomas_raw = request.POST.get('sintomas', '')
    sintomas = [s.strip() for s in sintomas_raw.split(',') if s.strip()]
    context = {}
    if "sintomas_seleccionadas" not in request.session:
        request.session["sintomas_seleccionadas"] = []
    if request.method == "POST":
        sintomas_seleccionados = request.POST.getlist("sintoma_seleccionado")
        sintomas_seleccionadas = request.session["sintomas_seleccionadas"]
        sintomas_seleccionados = [
            s for s in sintomas_seleccionados if s not in sintomas_seleccionadas]
        request.session["sintomas_seleccionadas"] += sintomas_seleccionados
        context["sintomas_seleccionadas"] = request.session["sintomas_seleccionadas"]
        context["sintomas"] = sintomas
        # Aquí puedes procesar los síntomas seleccionados según tus necesidades
        return render(request, "consultas/motivo_consulta.html", context)
        # return render(request, "consultas/motivo_consulta.html", context)
    return HttpResponse("Método no permitido.", status=405)


def vaciar_sintomas_seleccionados(request):
    request.session["sintomas_seleccionadas"] = []
    return redirect('motivo_consulta')


def motivo_consulta(request):
    context = {}
    if "sintomas" not in request.session:
        request.session["sintomas"] = ['fatiga', 'dolor de cabeza', 'mareos',
                'apnea del sueño', 'falta de energia', 'presion arterial alta']
    context["sintomas"] = request.session["sintomas"]
    if request.method == "POST":
        # Aquí puedes procesar los datos del motivo de consulta según tus necesidades
        motivo = request.POST.get('motivo', '').strip()
        observaciones = request.POST.get('observaciones', '')
        sintomas_observados = request.session.get("sintomas_seleccionadas", [])
        # return HttpResponse(f"Motivo: {motivo}, Observaciones: {observaciones}, Síntomas: {', '.join(sintomas_observados)}")
        return HttpResponse("motivo de consulta guardados correctamente.")

    return render(request, "consultas/motivo_consulta.html", context)
