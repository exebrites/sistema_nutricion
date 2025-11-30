import datetime
import json
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Alimento, Antropometria, Dieta, DietaAlimento, Paciente, Sintoma, MotivoConsulta, HabitoAlimentario
from .forms import AlimentoForm
from django.core.paginator import Paginator
# sistema experto
from experto.main import evaluar_nutricion, DiagnosticoPES
 

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
        apellido = request.POST.get("apellido")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        direccion_residencial = request.POST.get("direccion_residencial")
        numero_telefono = request.POST.get("numero_telefono")

        # 1. Aquí puedes guardar los datos del paciente en la base de datos
        # 2. Controlar que el nombre y apellido no existan en la base de datos
        paciente_existe = Paciente.objects.filter(
            nombre=nombre, apellido=apellido).first()
        if paciente_existe:
            context["error"] = "El paciente con nombre {} y apellido {} ya existe en la base de datos.".format(
                nombre, apellido)
            return render(request, "consultas/primera_consulta.html", context)
        try:
            paciente = Paciente.objects.create(
                nombre=nombre,
                apellido=apellido,
                sexo=sexo,
                edad=edad,
                fecha_nacimiento=fecha_nacimiento,
                direccion_residencial=direccion_residencial,
                numero_telefono=numero_telefono,
            )
            request.session["success"] = "Paciente creado exitosamente."
            request.session["paciente_id"] = paciente.id
        except Exception as e:
            return HttpResponse(f"Error al crear paciente: {e}", status=500)

        return redirect('motivo_consulta')

    return HttpResponse("Método no permitido.", status=405)


def agregar_sintoma_motivo_consulta(request):
    # texto: "fatiga,dolor de cabeza,..."
    sintomas = Sintoma.objects.all()
    context = {}
    if "sintomas_seleccionadas" not in request.session:
        request.session["sintomas_seleccionadas"] = []
    if request.method == "POST":
        id_sintoma_seleccionado = request.POST.getlist("sintoma_seleccionado")
        sintoma_seleccionado = Sintoma.objects.filter(
            id__in=id_sintoma_seleccionado)
        # agregar el sintoma seleccionado a la sesion y verifica duplicados
        # Obtener lista actual de la sesión
        sintomas_sesion = request.session["sintomas_seleccionadas"]
        ids_existentes = [s['id'] for s in sintomas_sesion]

        # Agregar solo los síntomas que no están duplicados
        for sintoma in sintoma_seleccionado:
            if sintoma.id not in ids_existentes:
                sintomas_sesion.append({
                    "id": sintoma.id,
                    "nombre": sintoma.nombre
                })
        request.session["sintomas_seleccionadas"] = sintomas_sesion

        # datos al template
        context["sintomas_seleccionadas"] = sintomas_sesion
        context["sintomas"] = sintomas
        # Aquí puedes procesar los síntomas seleccionados según tus necesidades
        return redirect('motivo_consulta')
        # return render(request, "consultas/motivo_consulta.html", context)
    return HttpResponse("Método no permitido.", status=405)


def vaciar_sintomas_seleccionados(request):
    request.session["sintomas_seleccionadas"] = []
    return redirect('motivo_consulta')


def motivo_consulta(request):
    # return HttpResponse("sintomas...")
    context = {}
    context = {'success': request.session['success']}
    # 1. eliminar el mensaje de exito de la sesion
    sintomas = Sintoma.objects.all()
    context["sintomas"] = sintomas
    # obtener sintomas seleccionados de la sesion
    if "sintomas_seleccionadas" not in request.session:
        request.session["sintomas_seleccionadas"] = []
    context["sintomas_seleccionadas"] = request.session["sintomas_seleccionadas"]

    # obtener pacientes y pasar
    pacientes = Paciente.objects.all()
    context["pacientes"] = pacientes

    # obtener paciente creado recientemente
    paciente_id = request.session.get("paciente_id")
    if paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        context["paciente"] = paciente
        # eliminar el id de la sesion
        del request.session["paciente_id"]

    if request.method == "POST":
        # Aquí puedes procesar los datos del motivo de consulta según tus necesidades

        motivo = request.POST.get('motivo', '').strip()
        observaciones = request.POST.get('observaciones', '')
        sintomas_observados = request.session.get("sintomas_seleccionadas", [])
        paciente_id = request.POST.get('paciente', '')
        paciente = get_object_or_404(Paciente, id=paciente_id)
        # Guardar el motivo de consulta y los síntomas en la base de datos

        try:
            motivo_consulta = MotivoConsulta.objects.create(
                paciente=paciente,
                motivo=motivo,
                observaciones=observaciones
            )
            for sintoma_data in sintomas_observados:
                sintoma = get_object_or_404(Sintoma, id=sintoma_data["id"])
                motivo_consulta.sintomas.add(sintoma)
            motivo_consulta.save()
            # Limpiar la lista de síntomas seleccionados en la sesión
            request.session["sintomas_seleccionadas"] = []
            request.session["paciente_id"] = paciente.id
        except Exception as e:

            return HttpResponse(f"Error al guardar el motivo de consulta: {e}", status=500)

        return redirect('alimentos_habitos')

    return render(request, "consultas/motivo_consulta.html", context)


def alimentos_habitos(request):
    context = {}
    # obtener alimento y enviarlos al templte
    alimentos = Alimento.objects.all()
    context["alimentos"] = alimentos
    # obtener alimentos seleccionados de la sesion
    if "lista_alimentos_seleccionados" not in request.session:
        request.session["lista_alimentos_seleccionados"] = []
    context["lista_alimentos_seleccionados"] = request.session["lista_alimentos_seleccionados"]
    # obtener habitos alimentarios y enviarlos al template
    habitos_alimentarios = HabitoAlimentario.objects.all()
    context["habitos_alimentarios"] = habitos_alimentarios
    # obtener el paciente
    paciente_id = request.session.get("paciente_id")
    if paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        context["paciente"] = paciente

    if request.method == "POST":
        # Aquí puedes procesar los datos de alimentos y hábitos según tus necesidades
        habito_alimenticio = request.POST.get('habitos', '').strip()
        lista_alimentos = request.session.get(
            "lista_alimentos_seleccionados", [])
        paciente_id = request.POST.get('paciente_id', '')
        paciente = get_object_or_404(Paciente, id=paciente_id)

        # Guardar los hábitos alimentarios y los alimentos en la base de datos
        try:
            # Aquí puedes guardar los datos en la base de datos según tu modelo
            dieta = Dieta.objects.create(
                nombre="Dieta del paciente",
                descripcion="Dieta creada durante la consulta",
                paciente=paciente,
            )
            for alimento_data in lista_alimentos:
                alimento = get_object_or_404(Alimento, id=alimento_data["id"])
                DietaAlimento.objects.create(
                    dieta=dieta,
                    alimento=alimento,
                    cantidad=0,
                    unidad='al'
                )
        except Exception as e:
            return HttpResponse(f"Error al guardar los datos: {e}", status=500)

        # return HttpResponse("Datos de alimentos y hábitos recibidos.")
        return redirect('crear_atropometria')
    return render(request, "consultas/alimentos_habitos.html", context)


def agregar_alimento(request):
    context = {}
    if request.method == "POST":
        alimento_seleccionado = request.POST.get("alimentos")
        if "lista_alimentos_seleccionados" not in request.session:
            request.session["lista_alimentos_seleccionados"] = []
        lista_alimentos_seleccionados = request.session["lista_alimentos_seleccionados"]
        if alimento_seleccionado not in [a["id"] for a in lista_alimentos_seleccionados]:
            alimento = Alimento.objects.get(id=alimento_seleccionado)
            consume = request.POST.get("consume") == "on"
            lista_alimentos_seleccionados.append({
                "id": alimento.id,
                "nombre": alimento.nombre,
                "consume": consume
            })
            request.session["lista_alimentos_seleccionados"] = lista_alimentos_seleccionados
            context = {
                "lista_alimentos_seleccionados": lista_alimentos_seleccionados
            }
            # return HttpResponse(json.dumps(context), content_type="application/json")
        return redirect('alimentos_habitos')

    return HttpResponse("Método no permitido.", status=405)


def vaciar_lista_alimentos_seleccionados(request):
    request.session["lista_alimentos_seleccionados"] = []
    return redirect('alimentos_habitos')


def crear_atropometria(request):
    context = {}
    if request.method == "POST":
        peso = request.POST.get("peso")
        altura = request.POST.get("altura")
        circunferencia_abdominal = request.POST.get("circunferencia_abdominal")
        paciente_id = request.session.get("paciente_id")
        paciente = get_object_or_404(Paciente, id=paciente_id)
        imc = None
        if peso and altura:
            try:
                peso_val = float(peso)
                altura_val = float(altura) / 100  # Convertir cm a metros
                imc = peso_val / (altura_val ** 2)
            except ValueError:
                imc = "Valores inválidos"
        context["imc"] = imc
        try:
            antropometria = Antropometria.objects.create(
                paciente=paciente,
                fecha_medicion=datetime.date.today(),
                peso_corporal=peso,
                altura=altura,
                imc=imc,
                perimetro_abdominal=float(
                    circunferencia_abdominal) if circunferencia_abdominal else None,
            )
        except Exception as e:
            return HttpResponse(f"Error al crear la antropometría: {e}", status=500)

        return redirect('informacion_general')
    return render(request, "consultas/antropometria.html", context)


def informacion_general(request):
    context = {}
    paciente_id = request.session.get("paciente_id")
    paciente = Paciente.objects.get(id=paciente_id)
    motivo_consulta = MotivoConsulta.objects.filter(
        paciente=paciente).last()
    antropometria = Antropometria.objects.filter(
        paciente=paciente).last()
    dieta = Dieta.objects.filter(paciente=paciente).last()
    # clasificar el imc sistema experto
  
    resultado, regla_activada = DiagnosticoPES.clasificar_imc(antropometria.imc)
    diagnostico_problema = {
        'explicacion': f"El paciente tiene un IMC de {antropometria.imc:.2f}, lo que lo clasifica como '{resultado}'.",
        'clasificacion': resultado,
        'regla_activada': regla_activada
    }
    
    context = {"paciente": paciente,
               "motivo_consulta": motivo_consulta,
               "antropometria": antropometria,
               "dieta": dieta,
               "diagnostico_problema": diagnostico_problema,
               }
    return render(request, "consultas/informacion_general.html", context)
