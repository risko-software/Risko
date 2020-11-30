import json
import os
import datetime
import requests as mi_requests
from json import dumps
from functools import wraps

from django.contrib.auth import logout as do_logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse

from Risk_project_ufps import my_constants
from Risk_project_ufps.core_risk.controller.ActividadController import ActividadController
from Risk_project_ufps.core_risk.controller import ComentarioController
from Risk_project_ufps.core_risk.controller.GerenteController import GerenteController
from Risk_project_ufps.core_risk.controller.LeccionController import LeccionController
from Risk_project_ufps.core_risk.controller.PaisController import PaisController
from Risk_project_ufps.core_risk.controller.ProyectoController import ProyectoController
from Risk_project_ufps.core_risk.controller.RbsController import RbsController
from Risk_project_ufps.core_risk.controller.RecursoController import RecursoController
from Risk_project_ufps.core_risk.controller.ReporteController import ReporteController
from Risk_project_ufps.core_risk.controller.ResponsableController import ResponsableController
from Risk_project_ufps.core_risk.controller.RespuestaController import RespuestaController
from Risk_project_ufps.core_risk.controller.RiesgoController import RiesgoController
from Risk_project_ufps.core_risk.controller.RolController import RolController
from Risk_project_ufps.core_risk.controller.SectorController import SectorController
from Risk_project_ufps.core_risk.controller.SubcategoriaController import SubcategoriaController
from Risk_project_ufps.core_risk.controller.TareaController import TareaController
from Risk_project_ufps.core_risk.controller.TipoRecursoController import TipoRecursoController
from Risk_project_ufps.core_risk.controller import VisitaController
from Risk_project_ufps.core_risk.dto.models import Actividad
from Risk_project_ufps.core_risk.dto.models import Categoria
from Risk_project_ufps.core_risk.dto.models import Proyecto
from Risk_project_ufps.core_risk.dto.models import Rbs
from Risk_project_ufps.core_risk.dto.models import SubCategoria


#########################################
# Sección para decoradores
#########################################

def validar_proyecto(function):
    def wrap(request, *args, **kwargs):
        proyecto_controller = ProyectoController()
        proyecto_id = kwargs['proyecto_id']
        gerente_id = request.user.id
        if proyecto_controller.is_owner(proyecto_id, gerente_id):
            return function(request, *args, **kwargs)
        else:
            return render(request, "error_acceso.html")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


#########################################
# Fin sección para decoradores
#########################################

"""
////////////////////////////////////////////////////////////////////////////
    Metodos generales de usuario
/////////////////////////////////////////////////////////////////////////////
"""


def index(request):
    VisitaController.crear_visita(datetime.datetime.now())
    nro_visitas = VisitaController.get_cantidad_visitas()
    proyecto_controller = ProyectoController()
    nro_proyectos = proyecto_controller.get_cantidad_proyectos()
    gerente_controller = GerenteController()
    nro_usuarios = gerente_controller.get_cantidad_gerente()

    if request.method == "POST":
        ComentarioController.crear_comentario(datetime.datetime.now(),
                                              request.POST["name"],
                                              request.POST["email"],
                                              request.POST["message"])
    return render(request, "index.html",
                  {"nro_visitas": nro_visitas, "nro_proyectos": nro_proyectos, "nro_usuarios": nro_usuarios})


# Autentica usuario y carga la vista de inicio
def autenticar(request):
    if request.user.is_authenticated:
        proyecto_controller = ProyectoController()
        lista_proyectos = proyecto_controller.listar_proyectos(request.user.id)
        return render(request, my_constants.INICIO_HTML, {"lista_proyectos": lista_proyectos})

    return render("login.html")


# Cierra sesión de un usuario y carga la vista de login
def cerrar_sesion(request):
    do_logout(request)
    return render(request, "login.html")


# Carga la vista de registrar gerente
def registrar_gerente(request):
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    pais_controller = PaisController()
    lista_paises = pais_controller.listar_paises()
    data = dict(lista_sectores=lista_sectores, lista_paises=lista_paises)
    mensaje_editar = request.GET.get("mensaje_editar")
    if mensaje_editar:
        data['mensaje_editar'] = mensaje_editar
    if os.environ['MODE_RECAPTCHA'] == 'True':
        key_recaptcha_front = os.environ['KEY_RECAPTCHA_FRONT']
        data['key_recaptcha_front'] = key_recaptcha_front
    return render(request, "registration/registrar_gerente.html", data)


# Duplica el usuario para accerder a los metodos de autenticación de django
def registrar_usuario(usuario, correo, password, nombre):
    user = User.objects.create_user(
        username=usuario,
        email=correo,
        password=password,
        first_name=nombre
    )
    user.save()
    return User.objects.get(username=usuario)


def registrar_nuevo_gerente(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.validar_gerente(request.POST["gerente_usuario"])
    if gerente == None:
        sector_controller = SectorController()
        sector = sector_controller.obtener_sector(request.POST["gerente_sector"])
        user = registrar_usuario(
            request.POST["gerente_usuario"],
            request.POST["gerente_correo"],
            request.POST["gerente_password"],
            request.POST["gerente_nombre"]
        )
        fecha_creacion = get_fecha_actual()
        mensaje = gerente_controller.registrar_gerente(
            user.id,
            request.POST["gerente_usuario"],
            request.POST["gerente_correo"],
            request.POST["gerente_nombre"],
            sector,
            request.POST["gerente_profesion"],
            request.POST["gerente_empresa"],
            request.POST["gerente_pais"],
            request.POST["metodologia"],
            request.POST["certificacion"],
            fecha_creacion
        )
        return render(request, "registration/login.html", {"mensaje": mensaje})
    sector_controller = SectorController()
    pais_controller = PaisController()

    lista_sectores = sector_controller.listar_sectores()
    lista_paises = pais_controller.listar_paises()

    url = reverse('registrargerente')
    mensaje_editar = "El usuario ya se encuentra registrado"
    url += "?mensaje_editar={}".format(mensaje_editar)
    return HttpResponseRedirect(url)


def nuevo_gerente(request):
    if os.environ['MODE_RECAPTCHA'] == 'True':
        recaptcha_response = request.POST["g-recaptcha-response"]
        if recaptcha_response and validar_captcha(recaptcha_response):
            return registrar_nuevo_gerente(request)
        else:
            url = reverse('registrargerente')
            mensaje_editar = "Captcha no valido"
            url += "?mensaje_editar={}".format(mensaje_editar)
            return HttpResponseRedirect(url)
    else:
        return registrar_nuevo_gerente(request)


def validar_captcha(recaptcha_response):
    flag = True
    if os.environ['MODE_RECAPTCHA'] == 'True':
        key_recaptcha_back = os.environ['KEY_RECAPTCHA_BACK']
        params = {'secret': key_recaptcha_back, 'response': recaptcha_response}
        url = "https://www.google.com/recaptcha/api/siteverify"
        try:
            rta = mi_requests.post(url, data=params)
            rta = rta.json()
            flag = rta['success']
        except mi_requests.exceptions.RequestException as e:
            print(e)
            flag = False
    return flag


# Muestra el perfil del gerente y actualiza su información
def mi_perfil(request):
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    if request.method == "POST":
        sector = sector_controller.obtener_sector(request.POST["gerente_sector"])
        request.user.first_name = request.POST["gerente_nombre"]
        request.user.email = request.POST["gerente_correo"]
        request.user.save()
        mensaje = gerente_controller.actualizar_gerente(gerente, request.POST["gerente_nombre"],
                                                        request.POST["gerente_correo"],
                                                        request.POST["gerente_profesion"],
                                                        request.POST["gerente_empresa"], sector,
                                                        request.POST["certificacion"],
                                                        request.POST["metodologia"])
        return render(request, "mi_perfil.html",
                      {"gerente": gerente, "lista_sectores": lista_sectores, "mensaje": mensaje})

    return render(request, "mi_perfil.html", {"gerente": gerente, "lista_sectores": lista_sectores})


# Carga la vista de inicio
# @login_required(login_url='/risko/accounts/login/')
def inicio(request):
    proyecto_controller = ProyectoController()
    lista_proyectos = proyecto_controller.listar_proyectos(request.user.id)

    return render(request, "inicio.html", {"lista_proyectos": lista_proyectos})


"""
////////////////////////////////////////////////
    Metodos y views relacionados con proyecto 
////////////////////////////////////////////////
"""


# Carga la vista de registrar proyecto y lo registra
def nuevo_proyecto(request):
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    fecha_actual = datetime.datetime.now()
    formato = "%Y-%m-%d"
    today = fecha_actual.strftime(formato)
    data = {"lista_sectores": lista_sectores, "today": today}
    rbs_controller = RbsController()
    rbs = rbs_controller.get_rbs_gerente_id(request.user.id)
    if rbs:
        data["rbs"] = rbs
    if (request.method == "POST"):
        proyecto_controller = ProyectoController()
        aux = proyecto_controller.validar_proyecto(request.POST["proyecto_nombre"], request.user.id)
        print(aux)
        if aux == None:
            try:
                gerente_controller = GerenteController()
                sector = sector_controller.obtener_sector(request.POST["proyecto_sector"])
                print("sector", sector)
                gerente = gerente_controller.obtener_gerente(request.user.id)

                proyecto = proyecto_controller.registrar_proyecto(
                    request.POST["proyecto_nombre"],
                    request.POST["proyecto_objetivo"],
                    request.POST["proyecto_alcance"],
                    request.POST["proyecto_descripcion"],
                    request.POST["proyecto_presupuesto"],
                    request.POST["proyecto_fecha_inicio"],
                    gerente,
                    sector
                )
                if (proyecto):
                    data["mensaje"] = "Se registro un proyecto exitosamente."
                else:
                    data["mensaje"] = "No se pudo registrar exitosamente."
                if (request.POST["actividades"] == '1'):
                    actividades = json.loads(request.POST["actividades_data"])["tasks"]
                    orden = 0
                    for actividad in actividades:
                        act = Actividad(
                            actividad_id="p_" + str(proyecto.proyecto_id) + "_a_" + str(actividad["id"]),
                            actividad_orden=orden,
                            actividad_uuid=actividad["uid"],
                            actividad_nombre=actividad["name"],
                            actividad_level=actividad["level"],
                            actividad_wbs=actividad["WBS"],
                            proyecto=proyecto,
                            actividad_fecha_inicio=actividad["start"],
                            actividad_fecha_fin=actividad["end"],
                            duracion=actividad["duration"],
                        )
                        act.save()
                        orden = orden + 1
                return render(request, "nuevo_proyecto.html", data)

            except Exception as inst:

                print(inst)
                raise inst
                return HttpResponse(status=400)

            data["mensaje"] = "El nombre del proyecto ya se encuentra en uso."

    return render(request, "nuevo_proyecto.html", data)


"""
/////////////////////////////////////
    Metodos de la EDR
////////////////////////////////////
"""


# Carga la vista de la RBS
def mi_rbs(request):
    rbs_controller = RbsController()
    if (rbs_controller.get_rbs_gerente_id(request.user.id)):
        return render(request, "mi_rbs.html")
    else:
        return render(request, "mi_rbs_inicial.html")


def rbs_configurar(request):
    rbs_controller = RbsController()
    if request.method == 'POST':
        rbs_option = request.POST.get('rbs_option', "")
        try:
            if rbs_option == "1":
                rbs_controller.crear_rbs_pmbok(request.user.id)
            elif rbs_option == "2":
                rbs_controller.crear_rbs_sugerida(request.user.id)
            elif rbs_option == "3":
                rbs_controller.crear_rbs_blanco(request.user.id)
            return HttpResponse({"msg": "rbs_creada"}, status=202)
        except Exception as inst:
            print(inst)
            return HttpResponse({"msg": "error"}, status=404)
    else:
        return HttpResponse({"msg": "error"}, status=404)


"""
////////////////////////////////////////////////
    Metodos relacionados con la rbs general
////////////////////////////////////////////////
"""


def profile(request):
    if request.method == 'GET':
        rbs_controller = RbsController()
        rbs = rbs_controller.obtener_rbs_general(request.user.id)
        return JsonResponse(rbs, safe=False)
    else:
        return HttpResponse(status=404)


def confirmar_cambios_rbs(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            acciones = json.loads(request.POST.get('acciones', None))
            rbs = Rbs.objects.get(gerente_id=request.user.id)
            elementos_nuevos = {}
            for accion in acciones:
                if accion['accion'] == 'agregar_c':
                    categoria = Categoria(
                        categoria_nombre=accion['categoria_nombre'],
                        categoria_descripcion=accion['categoria_descripcion'],
                        rbs=rbs
                    )
                    categoria.save()
                    elementos_nuevos[accion['categoria_id']] = categoria
                elif accion['accion'] == 'agregar_sc':
                    if ('new' in accion['categoria_id']):
                        categoria = elementos_nuevos[accion['categoria_id']]
                    else:
                        categoria = Categoria(categoria_id=accion['categoria_id'])
                    subCategoria = SubCategoria(
                        sub_categoria_nombre=accion['sub_categoria_nombre'],
                        sub_categoria_descripcion=accion['sub_categoria_descripcion'],
                        categoria=categoria
                    )
                    subCategoria.save()
                    elementos_nuevos[accion['sub_categoria_id']] = subCategoria
                elif accion['accion'] == 'eliminar_c':
                    if ('new' in accion['categoria_id']):
                        categoria = elementos_nuevos[accion['categoria_id']]
                        del elementos_nuevos[accion['categoria_id']]
                    else:
                        categoria = Categoria(categoria_id=accion['categoria_id'])
                    categoria.delete()
                elif accion['accion'] == 'eliminar_sc':
                    if ('new' in accion['sub_categoria_id']):
                        sub_categoria = elementos_nuevos[accion['sub_categoria_id']]
                        del elementos_nuevos[accion['sub_categoria_id']]
                    else:
                        sub_categoria = SubCategoria(sub_categoria_id=accion['sub_categoria_id'])
                    sub_categoria.delete()
                elif accion['accion'] == 'editar_c':
                    if ('new' in accion['categoria_id']):
                        categoria = elementos_nuevos[accion['categoria_id']]
                    else:
                        categoria = Categoria(categoria_id=accion['categoria_id'])
                    Categoria.objects.filter(categoria_id=categoria.categoria_id).update(
                        categoria_nombre=accion['categoria_nombre'],
                        categoria_descripcion=accion['categoria_descripcion'])
                elif accion['accion'] == 'editar_sc':
                    if ('new' in accion['sub_categoria_id']):
                        sub_categoria = elementos_nuevos[accion['sub_categoria_id']]
                    else:
                        sub_categoria = SubCategoria(sub_categoria_id=accion['sub_categoria_id'])
                    SubCategoria.objects.filter(sub_categoria_id=sub_categoria.sub_categoria_id).update(
                        sub_categoria_nombre=accion['sub_categoria_nombre'],
                        sub_categoria_descripcion=accion['sub_categoria_descripcion'])
            return JsonResponse({"hola": request.user.username, "e": acciones}, safe=False)
        else:
            return HttpResponse({"Error": "error"}, status=404)


# Carga la vista de nuevo riesgo y registra un riesgo asociado a una subcategoria
def nuevo_riesgo(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)
    if request.method == 'POST':
        subcategoria = subcategoria_controller.obtener_subcategoria(request.POST["sub_categoria_id"])
        riesgo_controller = RiesgoController()
        mensaje = riesgo_controller.registrar_riesgo(request.POST["riesgo_nombre"], request.POST["riesgo_causa"],
                                                     request.POST["riesgo_evento"], request.POST["riesgo_efecto"],
                                                     request.POST["riesgo_tipo"], subcategoria)
        return render(request, "nuevo_riesgo.html",
                      {"lista_subcategorias": lista_subcategorias, "rbs": rbsJSON, "mensaje": mensaje})

    return render(request, "nuevo_riesgo.html", {"lista_subcategorias": lista_subcategorias, "rbs": rbsJSON})


# Carga la tabla dinamica con el listado de riesgos
def mis_riesgos(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)
    return render(request, "mis_riesgos.html", {'rbs': rbsJSON, "lista_subcategorias": lista_subcategorias})


# Edita un riesgo de un gerente y carga el listado de riesgos
def editar_riesgo(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)

    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.listar_riesgos(request.user.id)
    riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])

    subcategoria = subcategoria_controller.obtener_subcategoria(request.POST["sub_categoria_id"])

    mensaje_editar = riesgo_controller.editar_riesgo(riesgo, request.POST["riesgo_nombre"],
                                                     request.POST["riesgo_causa"],
                                                     request.POST["riesgo_evento"], request.POST["riesgo_efecto"],
                                                     request.POST["riesgo_tipo"],
                                                     subcategoria)

    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)
    if request.method == 'POST':
        return render(request, my_constants.MIS_RIESGOS_HTML,
                      {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "mensaje_editar": mensaje_editar,
                       "lista_subcategorias": lista_subcategorias})

    return render(request, my_constants.MIS_RIESGOS_HTML,
                  {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "lista_subcategorias": lista_subcategorias})


# Elimina un riesgo de un gerente y carga el listado de riesgos
def eliminar_riesgo(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.listar_riesgos(request.user.id)
    riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
    mensaje_eliminar = riesgo_controller.eliminar_riesgo(riesgo)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)

    if request.method == 'POST':
        return render(request, my_constants.MIS_RIESGOS_HTML,
                      {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "mensaje_eliminar": mensaje_eliminar,
                       "lista_subcategorias": lista_subcategorias})

    return render(request, my_constants.MIS_RIESGOS_HTML,
                  {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "lista_subcategorias": lista_subcategorias})


@validar_proyecto
def asociar_riesgo(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    riesgo_controller = RiesgoController()
    if request.method == 'POST':
        try:
            riesgos_seleccionados = json.loads(request.POST.get('riesgos_seleccionados', None))
            riesgos_sugeridos = json.loads(request.POST.get('riesgos_sugeridos', None))
            aux = riesgo_controller.asosiar_riesgos_proyecto(riesgos_seleccionados, proyecto)
            aux = riesgo_controller.asosiar_riesgos_sugeridos_proyecto(riesgos_sugeridos, proyecto)
            return HttpResponse(status=200)
        except Exception as e:
            raise e
            return HttpResponse(status=400)

        # Carga la vista de nueva respuesta y registra una respuesta asociada a un riesgo


def nueva_respuesta(request):
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.listar_riesgos(request.user.id)

    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        respuesta = respuesta_controller.registrar_respuesta(request.POST["respuesta_nombre"],
                                                             request.POST["respuesta_descripcion"],
                                                             request.POST["tipo_respuesta"])

        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])

        mensaje = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)

        return render(request, "nueva_respuesta.html", {"lista_riesgos": lista_riesgos, "mensaje": mensaje})

    return render(request, "nueva_respuesta.html", {"lista_riesgos": lista_riesgos})


# Carga el listado de respuestas de un gerente
def mis_respuestas(request):
    respuesta_controller = RespuestaController()

    lista_riesgos_respuesta = respuesta_controller.listar_respuesta_riesgo(request.user.id)

    return render(request, "mis_respuestas.html", {"lista_riesgos_respuesta": lista_riesgos_respuesta})


# Elimina una respuesta y carga el listado de respuestas de un gerente
def eliminar_respuesta(request):
    respuesta_controller = RespuestaController()

    lista_riesgos_respuesta = respuesta_controller.listar_respuesta_riesgo(request.user.id)

    if request.method == 'POST':
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id_e"])

        mensaje_eliminar = respuesta_controller.eliminar_respuesta(respuesta)
        return render(request, my_constants.MIS_RESPUESTAS_HTML,
                      {"lista_riesgos_respuesta": lista_riesgos_respuesta, "mensaje_eliminar": mensaje_eliminar})

    return render(request, my_constants.MIS_RESPUESTAS_HTML, {"lista_riesgos_respuesta": lista_riesgos_respuesta})


# Actualiza la información de una respuesta y carga el listado de respuestas de un gerente
def editar_respuesta(request):
    respuesta_controller = RespuestaController()
    lista_riesgos_respuesta = respuesta_controller.listar_respuesta_riesgo(request.user.id)

    if request.method == 'POST':
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id"])

        mensaje_editar = respuesta_controller.editar_respuesta(respuesta, request.POST["respuesta_nombre"],
                                                               request.POST["respuesta_descripcion"],
                                                               request.POST["tipo_respuesta"])
        return render(request, my_constants.MIS_RESPUESTAS_HTML,
                      {"lista_riesgos_respuesta": lista_riesgos_respuesta, "mensaje_editar": mensaje_editar})

    return render(request, my_constants.MIS_RESPUESTAS_HTML, {"lista_riesgos_respuesta": lista_riesgos_respuesta})


# Carga la vista de roles del equipo
def roles_equipo(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    lista_roles_utilizados = rol_controller.lista_roles_utilizados(request.user.id)
    data = dict(
        lista_roles=lista_roles,
        lista_roles_utilizados=dumps(rol_controller.convert_to_dict(lista_roles_utilizados))
    )
    if 'mensaje' in request.GET:
        result = request.GET['mensaje']
        if result is not None and result != '':
            data['mensaje'] = result
    elif 'mensaje_error' in request.GET:
        result = request.GET['mensaje_error']
        if result is not None and result != '':
            data['mensaje_error'] = result
    elif 'mensaje_editar' in request.GET:
        result = request.GET['mensaje_editar']
        if result is not None and result != '':
            data['mensaje_editar'] = result
    elif 'mensaje_eliminar' in request.GET:
        result = request.GET['mensaje_eliminar']
        if result is not None and result != '':
            data['mensaje_eliminar'] = result

    return render(request, my_constants.ROLES_EQUIPO_HTML, data)


# Agrega un nuevo rol y carga la vista de roles de un gerente
def nuevo_rol(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    if request.method == 'POST':
        rol = rol_controller.registrar_rol(
            request.POST['rol_nombre'],
            request.POST['rol_descripcion'],
            gerente
        )
        mensaje = None
        if rol:
            mensaje = "?mensaje=Se registro el nuevo rol exitosamente."
        else:
            mensaje = "?mensaje_error=No se pudo registrar el nuevo rol."
    url_rta = reverse('roles_equipo') + mensaje
    return HttpResponseRedirect(url_rta)


# Actualiza la información de un rol y carga la vista de roles del gerente
def editar_rol(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        rol_editado = rol_controller.editar_rol(rol, request.POST['rol_nombre'], request.POST['rol_descripcion'])
        mensaje_editar = None
        if rol_editado:
            mensaje_editar = "?mensaje_editar=Se actualizo la información del rol exitosamente."
        else:
            mensaje_editar = "?mensaje_error=No se pudo actualizar la información del rol."
    url_rta = reverse('roles_equipo') + mensaje_editar
    return HttpResponseRedirect(url_rta)


# Elimina un rol y carga la vista de roles del gerente
def eliminar_rol(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        rol_eliminado = rol_controller.eliminar_rol(rol)
        mensaje = None
        if rol_eliminado == False:
            mensaje = "?mensaje_editar=No se pudo eliminar la información del rol."
        else:
            mensaje = "?mensaje_eliminar=Se elimino la información del rol exitosamente."
    url_rta = reverse('roles_equipo') + mensaje
    return HttpResponseRedirect(url_rta)


# Carga la vista de un proyecto y permite editarlo
@validar_proyecto
def mi_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    duracion = ""
    fecha_actual = datetime.datetime.now()
    fecha_proyecto = datetime.datetime(proyecto.proyecto_fecha_inicio.year, proyecto.proyecto_fecha_inicio.month,
                                       proyecto.proyecto_fecha_inicio.day, 00, 00, 00, 000000)
    if proyecto.proyecto_fecha_finl != None:
        fecha_proyecto_final = datetime.datetime(proyecto.proyecto_fecha_finl.year, proyecto.proyecto_fecha_finl.month,
                                                 proyecto.proyecto_fecha_finl.day, 00, 00, 00, 000000)

        dias = dias = abs((fecha_proyecto - fecha_proyecto_final).days)
        duracion = "El proyecto ya ha finalizado. Tuvo una duración de %i dias." % (dias)
    elif fecha_proyecto > fecha_actual:
        duracion = "El proyecto aun no ha iniciado."
    else:
        dias = abs((fecha_actual - fecha_proyecto).days)
        duracion = "%i dias." % (dias)

    data = {"proyecto": proyecto, "lista_sectores": lista_sectores, "duracion": duracion}

    if (proyecto_controller.has_actividades(proyecto_id)):
        data["actividades"] = True
        data["fecha_ultimo_cronograma"] = proyecto_controller.get_fecha_ultimo_cronograma(proyecto_id)

    if request.method == 'POST':
        sector = sector_controller.obtener_sector(request.POST["proyecto_sector"])
        mensaje = proyecto_controller.editar_proyecto(proyecto, request.POST["proyecto_nombre"],
                                                      request.POST["proyecto_objetivo"],
                                                      request.POST["proyecto_alcance"],
                                                      request.POST["proyecto_descripcion"],
                                                      request.POST["proyecto_presupuesto"],
                                                      request.POST["proyecto_fecha_inicio"], sector)
        data["mensaje"] = mensaje
        if request.POST["actividades"] == '1':
            actividades = json.loads(request.POST["actividades_data"])["tasks"]
            actividad_controller = ActividadController()
            actividad_controller.actualizar_actividades_proyecto(actividades, proyecto_id)
        return render(request, "procesos/proyecto.html", data)

    return render(request, "procesos/proyecto.html", data)


def eliminar_proyecto(request):
    proyecto_controller = ProyectoController()
    lista_proyectos = proyecto_controller.listar_proyectos(request.user.id)
    if request.method == 'POST':
        proyecto_id = request.POST["proyecto_id"]
        proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
        aux = proyecto_controller.eliminar_proyecto(proyecto)
        if aux is True:
            lista_proyectos = proyecto_controller.listar_proyectos(request.user.id)
            return render(request, my_constants.INICIO_HTML, {"lista_proyectos": lista_proyectos})
        return HttpResponseRedirect(reverse('mi_proyecto', args=(proyecto_id,)))
    return render(request, my_constants.INICIO_HTML, {"lista_proyectos": lista_proyectos})


@validar_proyecto
def eliminar_riesgo_proyecto(request, proyecto_id):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()
        riesgo_proyecto = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
        mensaje_eliminar = riesgo_controller.eliminar_riesgo_by_proyecto(riesgo_proyecto)

        proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
        rbs_controller = RbsController()
        rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
        rbsJSON = dumps(rbs)
        riesgo_controller = RiesgoController()
        lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)

        # Falta agregar de aqui para abajo
        responsable_controller = ResponsableController()
        lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
        actividad_controller = ActividadController()
        lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

        # Retorna responsables por riesgo de un proyecto
        responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
        # Retorna actividades por riesgo de un proyecto
        actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

        # (Funcion que retorna respuestas por riesgo de un proyecto (Revisar)!!!)
        respuesta_controller = RespuestaController()
        respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

        lista_riesgos_sugeridos = riesgo_controller.get_riesgos_sugeridos(proyecto.sector, request.user.id)
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


@validar_proyecto
def editar_riesgo_proyecto(request, proyecto_id):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()

        riesgo_editado = riesgo_controller.editar_riesgo_proyecto(
            proyecto_id,
            request.POST["riesgo_id_editar"],
            request.POST["riesgo_nombre"],
            request.POST["riesgo_causa"],
            request.POST["riesgo_evento"],
            request.POST["riesgo_efecto"],
            request.POST["riesgo_tipo"],
            # request.POST["riesgo_fecha_manifestacion"],
        )

        data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)

        return render(request, my_constants.IDENTIFICAR_RIESGOS_HTML, data)


################################################################
### Metodo util que permite centralizar los datos necesarios
### para renderizar identificar riesgos
################################################################

def get_data_render_identificar_riesgo(gerente_id, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(gerente_id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    # Falta agregar de aqui para abajo
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

    # Retorna responsables por riesgo de un proyecto
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    # Retorna actividades por riesgo de un proyecto
    actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    # (Funcion que retorna respuestas por riesgo de un proyecto (Revisar)!!!)
    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

    lista_riesgos_sugeridos = riesgo_controller.get_riesgos_sugeridos(proyecto.sector, gerente_id);

    if (len(lista_riesgos_sugeridos) > 0):
        return {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
                'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
                'lista_riesgos_sugeridos': lista_riesgos_sugeridos, 'respuestas_riesgo': respuestas_riesgo}

    return {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
            'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
            "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
            'respuestas_riesgo': respuestas_riesgo}


@validar_proyecto
def proyecto_nueva_respuesta(request, proyecto_id):
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)
    if request.method == 'POST':
        aux = respuesta_controller.validar_respuesta(request.POST["respuesta_nombre"], proyecto_id)
        if not aux:
            respuesta = respuesta_controller.registrar_respuesta(request.POST["respuesta_nombre"],
                                                                 request.POST["respuesta_descripcion"],
                                                                 "Eevitar")
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            mensaje_no = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)
            proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            mensaje = respuesta_controller.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta,
                                                                        request.POST["tipo_respuesta"])
            proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
            rbs_controller = RbsController()
            rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
            rbsJSON = dumps(rbs)
            riesgo_controller = RiesgoController()
            lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
            responsable_controller = ResponsableController()
            lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
            actividad_controller = ActividadController()
            lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto_id)
            responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
            actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto_id)

            data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)

            data['mensaje'] = mensaje

            return render(request, my_constants.IDENTIFICAR_RIESGOS_HTML, data)
        data['mensaje_editar'] = "Ya cuentas con esta respuesta asociada al proyecto."
        return render(request, my_constants.IDENTIFICAR_RIESGOS_HTML, data)

    return render(request, my_constants.IDENTIFICAR_RIESGOS_HTML, data)


def registrar_riesgo_proyecto(request):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()
        rbs_controller = RbsController()
        proyecto_controller = ProyectoController()

        mensaje = riesgo_controller.registrar_riesgo_proyecto(
            request.POST["riesgo_nombre"],
            request.POST["riesgo_causa"],
            request.POST["riesgo_evento"],
            request.POST["riesgo_efecto"],
            request.POST["riesgo_tipo"],
            request.POST["sub_categoria_id"],
            request.POST["proyecto_id"]
        )

        proyecto = proyecto_controller.obtener_proyecto(request.POST["proyecto_id"])
        rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto.proyecto_id)
        rbsJSON = dumps(rbs)
        riesgo_controller = RiesgoController()
        lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
        responsable_controller = ResponsableController()
        lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
        actividad_controller = ActividadController()
        lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto.proyecto_id)
        responsables_riesgo = riesgo_controller.listar_responsables_riesgo(proyecto.proyecto_id)
        actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto.proyecto_id)

        return render(request, my_constants.IDENTIFICAR_RIESGOS_HTML,
                      {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos, 'mensaje': mensaje,
                       'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                       "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo})


# Carga la vista de los recursos de un proyecto y registra nuevos recursos
@validar_proyecto
def recursos(request, proyecto_id):
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    data = dict(
        proyecto=proyecto,
        lista_recursos=lista_recursos,
        tipos_recursos=tipos_recursos
    )
    if 'result' in request.GET:
        result = request.GET['result']
        if result is not None and result != '':
            data['mensaje'] = result
    return render(request, my_constants.RECURSOS_HTML, data)


@validar_proyecto
def insertar_recurso(request, proyecto_id):
    if request.method == 'POST':
        recurso_controller = RecursoController()
        proyecto_controller = ProyectoController()
        proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
        mensaje = recurso_controller.registrar_recurso(
            proyecto,
            request.POST['recurso_nombre'],
            request.POST['recurso_costo'],
            request.POST['tipo_recurso_id']
        )
    url_rta = reverse('recursos', args=(proyecto_id,)) + "?result=" + mensaje
    return HttpResponseRedirect(url_rta)


# Elimina un recurso de un proyecto y carga la vista de recursos del proyecto
@validar_proyecto
def eliminar_recurso(request, proyecto_id):
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    if request.method == 'POST':
        recurso = recurso_controller.obtener_recurso(request.POST['recurso_id'])

        mensaje_eliminar = recurso_controller.eliminar_recurso(recurso)
        return render(request, my_constants.RECURSOS_HTML,
                      {"proyecto": proyecto, "lista_recursos": lista_recursos, "mensaje_eliminar": mensaje_eliminar,
                       "tipos_recursos": tipos_recursos})

    return render(request, my_constants.RECURSOS_HTML,
                  {"proyecto": proyecto, "lista_recursos": lista_recursos, "tipos_recursos": tipos_recursos})


# Actualiza la información de un recurso para un proyecto y carga la vista de recursos del proyecto
@validar_proyecto
def editar_recurso(request, proyecto_id):
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    if request.method == 'POST':
        recurso = recurso_controller.obtener_recurso(request.POST['recurso_id'])
        mensaje_editar = recurso_controller.editar_recurso(recurso, request.POST['recurso_nombre'],
                                                           request.POST['recurso_costo'],
                                                           request.POST['tipo_recurso_id'])
        return render(request, "procesos/mis_recursos.html",
                      {"proyecto": proyecto, "lista_recursos": lista_recursos, "mensaje_editar": mensaje_editar,
                       "tipos_recursos": tipos_recursos})

    return render(request, "procesos/mis_recursos.html",
                  {"proyecto": proyecto, "lista_recursos": lista_recursos, "tipos_recursos": tipos_recursos})


"""
////////////////////////////////////////////////////////////////////////////
    METODOS PARA PLANIFICAR PROYECTO
/////////////////////////////////////////////////////////////////////////////
"""


@validar_proyecto
def planificar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto_id)
    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)
    if rbs_proyecto:
        # No vacía
        return render(request, my_constants.PLANIFICAR_HTML,
                      {'proyecto': proyecto, 'rbs': True, 'rbs_proyecto': rp, 'rbs_sugerida': rs,
                       "lista_responsables": lista_responsables, "lista_roles": lista_roles, "impactos": impactos,
                       "probabilidades": probabilidades, "clasificacion_riesgo": clasificacion_riesgo})
    else:
        # Vacía
        return render(request, my_constants.PLANIFICAR_HTML,
                      {'proyecto': proyecto, 'rbs_proyecto': rp, 'rbs_sugerida': rs,
                       "lista_responsables": lista_responsables, "lista_roles": lista_roles, "impactos": impactos,
                       "probabilidades": probabilidades, "clasificacion_riesgo": clasificacion_riesgo})


@validar_proyecto
def planificar_proyecto_2(request, proyecto_id, mensaje):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto_id)
    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)
    if rbs_proyecto:
        # No vacía
        return render(
            request,
            my_constants.PLANIFICAR_HTML,
            {'proyecto': proyecto,
             'rbs': True,
             'rbs_proyecto': rp,
             'rbs_sugerida': rs,
             "lista_responsables": lista_responsables,
             "lista_roles": lista_roles,
             "impactos": impactos,
             "probabilidades": probabilidades,
             "clasificacion_riesgo": clasificacion_riesgo,
             "mensaje": mensaje
             })
    else:
        # Vacía
        return render(request, my_constants.PLANIFICAR_HTML,
                      {'proyecto': proyecto, 'rbs_proyecto': rp, 'rbs_sugerida': rs,
                       "lista_responsables": lista_responsables, "lista_roles": lista_roles, "impactos": impactos,
                       "probabilidades": probabilidades, "clasificacion_riesgo": clasificacion_riesgo,
                       "mensaje": mensaje})


def registrar_responsable(request):
    proyecto_controller = ProyectoController()
    proyecto_id = request.POST['proyecto_id']
    proyecto = proyecto_controller.obtener_proyecto(request.POST['proyecto_id'])
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(request.POST['proyecto_id'])
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(request.POST['proyecto_id'])
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        mensaje = responsable_controller.registrar_responsable(request.POST['nombre_responsable'],
                                                               request.POST['descripcion_responsable'],
                                                               proyecto.proyecto_id, rol)

        return HttpResponseRedirect(reverse('planificar_proyecto_2', args=(proyecto_id, mensaje)))

    return HttpResponseRedirect(reverse('mi_proyecto_planificar', args=(proyecto_id)))


def editar_responsable(request):
    responsable_controller = ResponsableController()
    responsable = responsable_controller.obtener_responsable(request.POST['responsable_id'])
    proyecto_id = request.POST['proyecto_id_editar']
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(responsable.proyecto_id)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto.proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)

    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        mensaje_editar = responsable_controller.editar_responsable(responsable, request.POST['responsable_nombre'],
                                                                   request.POST['responsable_descripcion'], rol)

        return render(request, "procesos/planificar.html",
                      dict(proyecto=proyecto,
                           rbs=True,
                           rbs_proyecto=rp,
                           rbs_sugerida=rs,
                           lista_responsables=lista_responsables,
                           mensaje_editar=mensaje_editar,
                           lista_roles=lista_roles,
                           impactos=impactos,
                           probabilidades=probabilidades,
                           clasificacion_riesgo=clasificacion_riesgo
                           )
                      )

    return render(request, "procesos/planificar.html",
                  dict(
                      proyecto=proyecto,
                      rbs=True,
                      rbs_proyecto=rp,
                      rbs_sugerida=rs,
                      lista_responsables=lista_responsables,
                      lista_roles=lista_roles,
                      impactos=impactos,
                      probabilidades=probabilidades,
                      clasificacion_riesgo=clasificacion_riesgo
                  )
                  )


def eliminar_responsable(request):
    responsable_controller = ResponsableController()
    responsable = responsable_controller.obtener_responsable(request.POST['responsable_id'])
    proyecto_id = request.POST['proyecto_id_el']
    lista_responsables = responsable_controller.listar_responsables(responsable.proyecto_id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(responsable.proyecto_id)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto.proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)

    if request.method == 'POST':
        mensaje_eliminar = responsable_controller.eliminar_responsable(responsable)
        return HttpResponseRedirect(reverse('mi_proyecto_planificar', args=(proyecto_id,)))

    return HttpResponseRedirect(reverse('mi_proyecto_planificar', args=(proyecto_id,)))


@validar_proyecto
def nuevo_responsable_riesgo(request, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    # Falta agregar de aqui para abajo
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto_id)
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto_id)

    if request.method == 'POST':
        responsable = responsable_controller.obtener_responsable(request.POST['responsable_id'])
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto.proyecto_id, riesgo.riesgo_id)

        mensaje = riesgo_controller.agregar_responsable_riesgo(proyecto_riesgo, responsable)
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


@validar_proyecto
def eliminar_responsable_riesgo(request, proyecto_id):
    if request.method == 'POST':
        responsable_id = request.POST['responsable_id']
        riesgo_id = request.POST['riesgo_id']
        responsable_controller = ResponsableController()
        responsable_controller.eliminar_responsable_riesgo(responsable_id, riesgo_id, proyecto_id)
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


@validar_proyecto
def nueva_actividad_riesgo(request, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

    if request.method == 'POST':
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto.proyecto_id, riesgo.riesgo_id)
        aux = actividad_controller.validar_actividad(proyecto_riesgo.proyecto_has_riesgo_id,
                                                     request.POST["actividad_id"])
        if aux == None:
            actividad = actividad_controller.obtener_actividad(request.POST["actividad_id"])
            mensaje = actividad_controller.registrar_actividad_riesgo(proyecto_riesgo, actividad)
            return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
        mensaje_editar = "Ya cuentas con esta actividad asignada al riesgo."
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


@validar_proyecto
def actualizar_definiciones_riesgo(request, proyecto_id):
    if request.method == "POST":
        proyecto_controller = ProyectoController()
        definiciones = filtrar_definiciones(request)
        impactos = definiciones["impactos"]
        probabilidades = definiciones["probabilidades"]
        proyecto_controller.actualizar_impactos_by_proyecto_id(impactos, proyecto_id)
        proyecto_controller.actualizar_probabilidades_by_proyecto_id(probabilidades, proyecto_id)
    return HttpResponseRedirect(reverse('mi_proyecto_planificar', args=(proyecto_id,)))


def filtrar_definiciones(request):
    impactos = []
    probabilidades = []
    for key, value in request.POST.items():
        if ('impacto_nombre_' in key):
            x = key.split("_")[2]
            impactos.append({
                "nombre": value,
                "valor": request.POST.get('impacto_valor_' + str(x)),
                "id": request.POST.get('impacto_id_' + str(x))
            })
        elif ('propabilida_nombre_' in key):
            x = key.split("_")[2]
            probabilidades.append({
                "nombre": value,
                "valor": request.POST.get('propabilida_valor_' + str(x)),
                "id": request.POST.get('propabilidad_id_' + str(x))
            })
    return {"impactos": impactos, "probabilidades": probabilidades}


@validar_proyecto
def actualizar_clasificacion_riesgo(request, proyecto_id):
    if request.method == "POST":
        proyecto_controller = ProyectoController()
        clasificaciones = filtrar_clasificaciones(request)
        proyecto_controller.actualizar_clasificacion_riesgo_by_proyecto_id(clasificaciones, proyecto_id)
    return HttpResponseRedirect(reverse('mi_proyecto_planificar', args=(proyecto_id,)))


def filtrar_clasificaciones(request):
    aux = []
    for key, value in request.POST.items():
        if 'clasificacion_nombre' in key:
            x = key.split("_")[2]
            aux.append({
                "nombre": value,
                "color": request.POST.get('clasificacion_color_' + str(x)),
                "valor_min": request.POST.get('clasificacion_min_' + str(x)),
                "valor_max": request.POST.get('clasificacion_max_' + str(x)),
            })
    return aux


"""
////////////////////////////////////////////////////////////////////////////
    METODOS PARA IDENTIFICAR RIESGOS DEL PROYECTO
/////////////////////////////////////////////////////////////////////////////
"""


@validar_proyecto
def identificar_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)

    # Falta agregar de aqui para abajo
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

    # Retorna responsables por riesgo de un proyecto
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    # Retorna actividades por riesgo de un proyecto
    actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    # (Funcion que retorna respuestas por riesgo de un proyecto (Revisar)!!!)
    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

    lista_riesgos_sugeridos = riesgo_controller.get_riesgos_sugeridos(proyecto.sector, request.user.id)

    if (len(lista_riesgos_sugeridos) > 0):
        return render(request, "procesos/identificar_riesgos.html",
                      {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
                       'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                       "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
                       'lista_riesgos_sugeridos': lista_riesgos_sugeridos, 'respuestas_riesgo': respuestas_riesgo})

    return render(request, "procesos/identificar_riesgos.html",
                  {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
                   'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                   "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
                   'respuestas_riesgo': respuestas_riesgo})


@validar_proyecto
def eliminar_actividad_proyecto(request, proyecto_id):
    data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)
    if request.method == 'POST':
        actividad_controller = ActividadController()
        actividad = actividad_controller.desasociar_actividad_riesgo(proyecto_id, request.POST['riesgo_id_actividad'],
                                                                     request.POST['actividad_id_riesgo'])
        if (actividad):
            data["mensaje_eliminar"] = "Eliminado"
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


@validar_proyecto
def nueva_respuesta_identificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    if request.method == 'POST':
        # Valida que una respuesta no se llame igual en el mismo proyecto (No se si deberia ser asi)
        aux = respuesta_controller.validar_respuesta(request.POST["respuesta_nombre"], proyecto_id)
        if not aux:
            respuesta = respuesta_controller.registrar_respuesta(
                request.POST["respuesta_nombre"],
                request.POST["respuesta_descripcion"],
                request.POST["tipo_respuesta"]
            )
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            mensaje_no = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)
            proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            mensaje = respuesta_controller.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta,
                                                                        request.POST["tipo_respuesta"])

            respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


@validar_proyecto
def desasociar_respuesta_identificar(request, proyecto_id):
    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        riesgo_id = request.POST["riesgo_id_eliminar"]
        respuesta_id = request.POST['respuesta_id_eliminar']

        respuesta_controller.desasociar_respuesta_riesgo_by_proyecto(respuesta_id, riesgo_id, proyecto_id)

    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


"""
////////////////////////////////////////////////////////////////////////////
    METODOS DE EVALUAR RIESGOS
/////////////////////////////////////////////////////////////////////////////
"""


@validar_proyecto
def evaluar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = dumps(riesgo_controller.get_riesgos_by_proyecto_2(proyecto))

    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))

    valores = dumps(get_valores_by_proyecto(proyecto_id))
    return render(request, "procesos/evaluar.html",
                  {'proyecto': proyecto, 'lista_riesgos': lista_riesgos, 'valores': valores, 'rangos': rangos})


def get_valores_by_proyecto(proyecto_id):
    proyecto_controller = ProyectoController()
    impactos = proyecto_controller.obtener_impactos_parseados_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_parseados_by_proyecto_id(proyecto_id)
    impactos.update(probabilidades)
    return impactos


def get_valores_by_proyecto_linea(proyecto_id, linea_base):
    proyecto_controller = ProyectoController()
    impactos = proyecto_controller.obtener_impactos_parseados_by_proyecto_id_linea(proyecto_id, linea_base)
    probabilidades = proyecto_controller.obtener_probabilidades_parseados_by_proyecto_id_linea(proyecto_id, linea_base)
    impactos.update(probabilidades)
    return impactos


@validar_proyecto
def actualizar_valores(request, proyecto_id):
    if request.method == 'POST':
        proyecto_controller = ProyectoController()
        valores = json.loads(request.POST["valores"])
        # try:
        proyecto_controller.actualizar_valores_riesgo_proyecto(valores, proyecto_id)
        # except Exception as e:
        #    print(e)
        #   return HttpResponse(status=500)
        return HttpResponse(status=200)
    return HttpResponse(status=500)


"""
////////////////////////////////////////////////////////////////////////////
    METODOS DE PLANIFICAR RESPUESTAS
/////////////////////////////////////////////////////////////////////////////
"""


def get_data_planificar_respuesta(proyecto_id: int):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    actividad_controller = ActividadController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)

    riesgos_evaluados = riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id)
    valores = get_valores_by_proyecto(proyecto_id)

    lista_riesgos = sort_riesgos_by_evaluacion(lista_riesgos, riesgos_evaluados, valores['impactos'],
                                               valores['probabilidades'])

    riesgos_evaluados = dumps(riesgos_evaluados)
    valores = dumps(valores)

    actividades_by_riesgos = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    # Listado de respuestas por riesgo, reutilizado de identificar
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    recurso_controller = RecursoController()
    # Recursos generales del proyecto
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    # Tareas por acciones por riesgo del proyecto
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    # Este metodo me lo invente para no tener que volver a consultar los los riesgos de un proyecto
    # Entre menos llamados a los metodos que hacen innerjoin mucho mejor
    # riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))

    linea_base = crear_arreglo_linea_base(proyecto_id)

    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

    return dict(
        proyecto=proyecto,
        lista_riesgos=lista_riesgos,
        respuestas_riesgo=respuestas_riesgo,
        lista_recursos=lista_recursos,
        lista_tareas=lista_tareas,
        respuestas_sugeridas=respuestas_sugeridas,
        riesgos_evaluados=riesgos_evaluados,
        rangos=rangos,
        valores=valores,
        linea_base=linea_base,
        actividades_by_riesgos=actividades_by_riesgos
    )


def sort_riesgos_by_evaluacion(riesgos, riesgos_evaluados, impactos, probabilidades):
    """ Mi intención consistia en ahorrarme un inner join, ahora me di cuenta que fue una
        mala idea. por esa razon es que existe este metodo. Ahora me toca evaluar los metodos
        y ordenarlos para que esten de mayor a menor, pido disculpas por las molestias
    """
    for riesgo in riesgos:
        key = "riesgo_" + str(riesgo['riesgo_id'])
        evaluacion = riesgos_evaluados[key]
        impacto = get_impacto_escala_by_id(impactos, evaluacion['impacto_id'])
        probabilidad = get_probabilidad_escala_by_id(probabilidades, evaluacion['propabilidad_id'])
        riesgo['riesgo_prom_evaluacion'] = int(impacto) * int(probabilidad)
    riesgos = sorted(riesgos, key=lambda riesgo: riesgo['riesgo_prom_evaluacion'], reverse=True)
    return riesgos


def get_impacto_escala_by_id(impactos, impacto_id):
    value = 0
    for impacto in impactos:
        if impacto['id'] == impacto_id:
            value = impacto['escala']
            break
    return value


def get_probabilidad_escala_by_id(probabilidades, probabilidad_id):
    value = 0
    for probabilidad in probabilidades:
        if probabilidad['id'] == probabilidad_id:
            value = probabilidad['escala']
            break
    return value


def crear_arreglo_linea_base(proyecto_id):
    proyecto_controller = ProyectoController()
    arreglo = proyecto_controller.get_lineas_base(proyecto_id)
    for proyecto in arreglo:
        aux = proyecto.proyecto_fecha_linea_base
        formato = "%d-%m-%Y"
        nueva_fecha = aux.strftime(formato)
        proyecto.proyecto_fecha_linea_base = nueva_fecha

    return arreglo


@validar_proyecto
def planificar_respuestas(request, proyecto_id):
    # proyecto = Proyecto.objects.using('base').get(proyecto_id=2, proyecto_linea_base=1)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base
    return render(
        request,
        my_constants.PLANIFICAR_RESPUESTAS_HTML,
        get_data_planificar_respuesta(proyecto_id)
    )


@validar_proyecto
def planificar_respuestas_2(request, proyecto_id, mensaje, mensaje_editar):
    # proyecto = Proyecto.objects.using('base').get(proyecto_id=2, proyecto_linea_base=1)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base
    data = get_data_planificar_respuesta(proyecto_id)
    if mensaje_editar == 'NONE':
        data['mensaje'] = mensaje
    else:
        data['mensaje_editar'] = mensaje_editar
    return render(
        request,
        my_constants.PLANIFICAR_RESPUESTAS_HTML,
        data
    )


def nueva_respuesta_planificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    data = get_data_planificar_respuesta(proyecto_id)

    if request.method == 'POST':
        # Valida que una respuesta no se llame igual en el mismo proyecto (No se si deberia ser asi)
        aux = respuesta_controller.validar_respuesta(request.POST["respuesta_nombre"], proyecto_id)
        if not aux:
            respuesta = respuesta_controller.registrar_respuesta(
                request.POST["respuesta_nombre"],
                request.POST["respuesta_descripcion"],
                request.POST["tipo_respuesta"]
            )
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            mensaje_no = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)
            proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            mensaje = respuesta_controller.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta,
                                                                        request.POST["tipo_respuesta"])

            data['mensaje'] = mensaje
            respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
            data['respuestas_riesgo'] = respuestas_riesgo
            return render(
                request,
                my_constants.PLANIFICAR_RESPUESTAS_HTML,
                data
            )
        data['mensaje_editar'] = "Ya cuentas con esta respuesta asociada al proyecto."
        return render(
            request,
            my_constants.PLANIFICAR_RESPUESTAS_HTML,
            data
        )

    return render(
        request,
        my_constants.PLANIFICAR_RESPUESTAS_HTML,
        data
    )


@validar_proyecto
def asociar_respuesta_sugeridas(request, proyecto_id):
    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        riesgo_id = request.POST["riesgo_id_rta"]
        respuestas_id = filtrar_respuestas_id_from_request(request)

        respuestas = respuesta_controller.registrar_respuesta_sugeridas_riesgo(respuestas_id, riesgo_id, proyecto_id)

    return HttpResponseRedirect(reverse('planificar_respuestas', args=(proyecto_id,)))


@validar_proyecto
def editar_respuesta_planificar(request, proyecto_id):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()
        respuesta_controller = RespuestaController()
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id"])
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        mensaje_editar = respuesta_controller.editar_respuesta(respuesta, request.POST["respuesta_nombre"],
                                                               request.POST["respuesta_descripcion"])
        proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, riesgo.riesgo_id)
        riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
        respuesta_proyecto = respuesta_controller.get_riesgo_respuesta_by_id(proyecto_riesgo, riesgo_respuesta)
        print(respuesta_proyecto)
        mensaje_editar = respuesta_controller.actualizar_tipo_respuesta(respuesta_proyecto,
                                                                        request.POST["tipo_respuesta"])
    return HttpResponseRedirect(reverse('planificar_respuestas', args=(proyecto_id,)))


@validar_proyecto
def desasociar_respuesta_riesgo(request, proyecto_id):
    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        riesgo_id = request.POST["riesgo_id_eliminar"]
        respuesta_id = request.POST['respuesta_id_eliminar']

        respuesta_controller.desasociar_respuesta_riesgo_by_proyecto(respuesta_id, riesgo_id, proyecto_id)

    return HttpResponseRedirect(reverse('planificar_respuestas', args=(proyecto_id,)))


def filtrar_respuestas_id_from_request(request):
    aux = []
    for key, value in request.POST.items():
        if 'respuesta_sugerida_' in key:
            aux.append(value)
    return aux


@validar_proyecto
def nueva_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))
    if request.method == 'POST':
        # Esto valida el nombre, pero en vista de las circustancias quite la validacion
        # aux = tarea_controller.validar_tarea(request.POST["tarea_nombre"], request.POST["respuesta_id"], proyecto)
        # if not aux:
        riesgo_proyecto = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id"])
        riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
        proyecto_riesgo_respuesta = respuesta_controller.get_riesgo_respuesta_by_id(riesgo_proyecto,
                                                                                    riesgo_respuesta)

        tarea = tarea_controller.registrar_tarea(
            proyecto_riesgo_respuesta,
            request.POST["tarea_nombre"],
            request.POST["tarea_descripcion"],
            request.POST["tarea_fecha_inicio"],
            request.POST["tarea_fecha_fin"],
            request.POST["tarea_fecha_inicio"],
            request.POST["tarea_fecha_fin"]
        )
        fecha_ini = datetime.datetime.strptime(request.POST["tarea_fecha_inicio"], my_constants.FORMATO_DATE_DESC)
        fecha_final = datetime.datetime.strptime(request.POST["tarea_fecha_fin"], my_constants.FORMATO_DATE_DESC)
        semanas = abs((fecha_ini - fecha_final).days) / 7
        dias = abs((fecha_ini - fecha_final).days)  # perdoname niñita
        tarea.duracion = dias
        tarea.duracion_real = dias
        tarea.save()
        lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
        if tarea == None:
            mensaje_editar = "No se pudo registrar la tarea."
            return HttpResponseRedirect(reverse('planificar_respuestas_2', args=(proyecto_id, '_', mensaje_editar)))
        else:
            mensaje = "Nueva tarea registrada."
            return HttpResponseRedirect(reverse('planificar_respuestas_2', args=(proyecto_id, mensaje, 'NONE')))
    return HttpResponseRedirect(reverse('planificar_respuestas', args=(proyecto_id,)))


@validar_proyecto
def eliminar_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    actividad_controller = ActividadController()
    actividades_by_riesgos = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))
    linea_base = crear_arreglo_linea_base(proyecto.proyecto_id)
    if request.method == 'POST':
        tarea = tarea_controller.get_tarea_by_id(request.POST["tarea_id"])
        mensaje_eliminar = tarea_controller.eliminar_tarea(tarea)
        lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
        return render(
            request,
            my_constants.PLANIFICAR_RESPUESTAS_HTML,
            dict(
                proyecto=proyecto,
                lista_riesgos=lista_riesgos,
                respuestas_riesgo=respuestas_riesgo,
                lista_recursos=lista_recursos,
                lista_tareas=lista_tareas,
                respuestas_sugeridas=respuestas_sugeridas,
                riesgos_evaluados=riesgos_evaluados,
                rangos=rangos,
                valores=valores,
                mensaje_eliminar=mensaje_eliminar,
                linea_base=linea_base,
                actividades_by_riesgos=actividades_by_riesgos

            )
        )

    return render(
        request,
        my_constants.PLANIFICAR_RESPUESTAS_HTML,
        dict(
            proyecto=proyecto,
            lista_riesgos=lista_riesgos,
            respuestas_riesgo=respuestas_riesgo,
            lista_recursos=lista_recursos,
            lista_tareas=lista_tareas,
            respuestas_sugeridas=respuestas_sugeridas,
            riesgos_evaluados=riesgos_evaluados,
            rangos=rangos,
            valores=valores,
            linea_base=linea_base,
            actividades_by_riesgos=actividades_by_riesgos

        )
    )


@validar_proyecto
def editar_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))
    actividad_controller = ActividadController()
    actividades_by_riesgos = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))
    linea_base = crear_arreglo_linea_base(proyecto.proyecto_id)

    if request.method == 'POST':
        tarea = tarea_controller.get_tarea_by_id(request.POST["tarea_id"])
        tarea_editada = tarea_controller.editar_tarea(tarea, request.POST["tarea_nombre"],
                                                      request.POST["descripcion_tarea"],
                                                      request.POST["tarea_fecha_inicio"],
                                                      request.POST["tarea_fecha_fin"])

        fecha_ini = datetime.datetime.strptime(request.POST["tarea_fecha_inicio"], '%Y-%m-%d')
        fecha_final = datetime.datetime.strptime(request.POST["tarea_fecha_fin"], '%Y-%m-%d')
        dias = abs((fecha_ini - fecha_final).days)
        tarea_editada.duracion = dias
        tarea_editada.duracion_real = dias
        tarea_editada.save()
        mensaje_editar = "Se actualizó la tarea exitosamente."
        lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))

        return render(
            request,
            my_constants.PLANIFICAR_RESPUESTAS_HTML,
            dict(
                proyecto=proyecto,
                lista_riesgos=lista_riesgos,
                respuestas_riesgo=respuestas_riesgo,
                lista_recursos=lista_recursos,
                lista_tareas=lista_tareas,
                respuestas_sugeridas=respuestas_sugeridas,
                riesgos_evaluados=riesgos_evaluados,
                rangos=rangos,
                valores=valores,
                linea_base=linea_base,
                mensaje_editar=mensaje_editar,
                actividades_by_riesgos=actividades_by_riesgos
            )
        )

    return render(
        request,
        my_constants.PLANIFICAR_RESPUESTAS_HTML,
        dict(
            proyecto=proyecto,
            lista_riesgos=lista_riesgos,
            respuestas_riesgo=respuestas_riesgo,
            lista_recursos=lista_recursos,
            lista_tareas=lista_tareas,
            respuestas_sugeridas=respuestas_sugeridas,
            riesgos_evaluados=riesgos_evaluados,
            linea_base=linea_base,
            rangos=rangos,
            valores=valores,
            actividades_by_riesgos=actividades_by_riesgos
        )
    )


@validar_proyecto
def nuevo_recurso_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    recurso_controller = RecursoController()
    data = get_data_planificar_respuesta(proyecto_id)
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    if request.method == 'POST':
        tarea_controller = TareaController()
        respuesta_controller = RespuestaController()
        tarea = tarea_controller.get_tarea_by_id(request.POST["tarea_id"])
        recurso = recurso_controller.obtener_recurso(request.POST["recurso_id"])

        aux = tarea_controller.get_recurso_tarea_by_id(tarea, recurso)

        if aux is None:
            mensaje = tarea_controller.agregar_recurso_tarea(tarea, recurso, request.POST["recurso_cantidad"])
            data['mensaje'] = mensaje
        else:
            mensaje_editar = "Ya cuentas con este recurso asignado a la tarea."
            data['mensaje_editar'] = mensaje_editar

        data["respuestas_riesgo"] = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
        data["lista_tareas"] = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
        data["lista_recursos"] = recurso_controller.listar_recursos(proyecto_id)

    return render(
        request,
        "procesos/planificar_respuestas.html",
        data
    )


@validar_proyecto
def desvincular_recurso_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    recurso_controller = RecursoController()
    tarea_controller = TareaController()
    data = get_data_planificar_respuesta(proyecto_id)

    if request.method == 'POST':
        tarea_id = request.POST["tarea_id"]
        recurso_id = request.POST["recurso_id"]
        mensaje_eliminar = tarea_controller.eliminar_recurso_tarea_2(recurso_id, tarea_id)
        data = get_data_planificar_respuesta(proyecto_id)
        data['lista_recursos'] = recurso_controller.listar_recursos(proyecto_id)
        data['mensaje_eliminar'] = mensaje_eliminar

    return render(
        request,
        "procesos/planificar_respuestas.html",
        data
    )


@validar_proyecto
def linea_base(request, proyecto_id, numero_linea, fecha_linea):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()

    # proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    proyecto = proyecto_controller.obtener_proyecto_by_proyecto_id_and_linea_base(proyecto_id, numero_linea)
    if proyecto:
        lista_riesgos = riesgo_controller.get_riesgos_by_proyecto_linea(proyecto, numero_linea)  # En teoria ya
        riesgos_evaluados = riesgo_controller.evaluar_riesgos_by_proyecto_id_linea(lista_riesgos, proyecto_id,
                                                                                   numero_linea)
        valores = get_valores_by_proyecto_linea(proyecto_id, numero_linea)  # Este
        valores = dumps(valores)
        riesgos_evaluados = dumps(riesgos_evaluados)
        # Listado de respuestas por riesgo, reutilizado de identificar
        respuestas_riesgo = dumps(
            respuesta_controller.listar_riesgos_respuesta_linea(proyecto_id, numero_linea))  # En teoria ya
        recurso_controller = RecursoController()
        # Recursos generales del proyecto
        lista_recursos = recurso_controller.listar_recursos_linea(proyecto_id, numero_linea)  # En teoria ya
        tarea_controller = TareaController()
        # El proyecto trae la ultima linea base, por esa razon se le debe indicar la que es
        proyecto.proyecto_linea_base = numero_linea
        # Tareas por acciones por riesgo del proyecto
        lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo_base(proyecto))
        # lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo_linea(proyecto, numero_linea))  # En teoria ya
        # Este metodo me lo invente para no tener que volver a consultar los los riesgos de un proyecto
        # Entre menos llamados a los metodos que hacen innerjoin mucho mejor
        rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id_linea(proyecto_id,
                                                                                         numero_linea))  # En teoria ya
        linea_base = crear_arreglo_linea_base(proyecto.proyecto_id)
        data = dict(
            proyecto=proyecto,
            lista_riesgos=lista_riesgos,
            respuestas_riesgo=respuestas_riesgo,
            lista_recursos=lista_recursos,
            lista_tareas=lista_tareas,
            riesgos_evaluados=riesgos_evaluados,
            rangos=rangos,
            valores=valores,
            linea_base=linea_base,
            numero_linea=numero_linea,
            fecha_linea=fecha_linea
        )
        return render(request, "procesos/linea_base.html", data)
    else:
        return render(request, "error_proyecto_base.html")


"""
////////////////////////////////////////////////////////////////////////////
    METODOS CONTROLAR RIESGOS
/////////////////////////////////////////////////////////////////////////////
"""


@validar_proyecto
def controlar_riesgos(request, proyecto_id):
    proyecto_controller = ProyectoController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    return render(
        request,
        "procesos/controlar_riesgos.html",
        dict(
            proyecto=proyecto,
        )
    )


@validar_proyecto
def crear_linea_base(request, proyecto_id):
    proyecto_controller = ProyectoController()
    gerente_id = request.user.id
    rta = proyecto_controller.crear_linea_base(gerente_id, proyecto_id)
    if rta:
        return HttpResponse({'rta': rta}, status=200)
    else:
        return HttpResponse({'rta': rta}, status=500)


@validar_proyecto
def actualizar_gantt(request, proyecto_id):
    proyecto_controller = ProyectoController()
    gantt = json.loads(request.POST['gantt'])
    rta = proyecto_controller.actualizar_gantt(proyecto_id, gantt)
    if rta:
        return HttpResponse({'rta': rta}, status=200)
    else:
        return HttpResponse({'rta': rta}, status=500)


@validar_proyecto
def obtener_tree_grid(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    tarea_controller = TareaController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = dumps(riesgo_controller.get_riesgos_by_proyecto_base_with_tareas(proyecto))
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta_base(proyecto_id))
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo_base(proyecto))

    return render(
        request,
        "procesos/cuadro.html",
        dict(
            proyecto=proyecto,
            lista_riesgos=lista_riesgos,
            respuestas_riesgo=respuestas_riesgo,
            lista_tareas=lista_tareas
        )
    )


"""
////////////////////////////////////////////////////////////////////////////
    METODOS CERRAR PROYECTO
/////////////////////////////////////////////////////////////////////////////
"""


@validar_proyecto
def cerrar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    leccion_controller = LeccionController()
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)
    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones

    )

    if request.method == 'POST':
        fecha_actual = datetime.datetime.now()
        aux = proyecto_controller.cerrar_proyecto(proyecto, fecha_actual)
        data['mensaje_eliminar'] = "Se ha finalizado la gestión de riesgos de forma exitosa."

    return render(
        request,
        my_constants.CERRAR_PROYECTO_HTML,
        data
    )


@validar_proyecto
def registrar_leccion(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    leccion_controller = LeccionController()
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)

    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones
    )

    if request.method == 'POST':
        leccion = leccion_controller.registrar_leccion(proyecto, request.POST["descripcion_leccion"])
        return HttpResponseRedirect(reverse('cerrar_proyecto', args=(proyecto_id,)))
    else:
        return HttpResponseRedirect(reverse('cerrar_proyecto', args=(proyecto_id,)))


@validar_proyecto
def eliminar_leccion(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    leccion_controller = LeccionController()
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)

    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones
    )

    if request.method == 'POST':

        leccion = leccion_controller.get_leccion_by_id(request.POST["leccion_id"])
        if leccion != None:
            data['mensaje_eliminar'] = leccion_controller.eliminar_leccion(leccion)
            return render(
                request,
                my_constants.CERRAR_PROYECTO_HTML, data
            )

        data['mensaje_editar'] = "Esta lección ya ha sido eliminada."
        return render(
            request,
            my_constants.CERRAR_PROYECTO_HTML, data
        )

    return render(
        request,
        my_constants.CERRAR_PROYECTO_HTML, data
    )


@validar_proyecto
def editar_leccion(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    leccion_controller = LeccionController()
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)

    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones
    )

    if request.method == 'POST':

        leccion = leccion_controller.get_leccion_by_id(request.POST["leccion_id"])
        if leccion != None:
            data['mensaje_editar'] = leccion_controller.editar_leccion(leccion, request.POST["descripcion_leccion"])
            return render(
                request,
                my_constants.CERRAR_PROYECTO_HTML, data
            )

        data['mensaje_editar'] = "No se ha encontrado la lección que se intenta editar."
        return render(
            request,
            my_constants.CERRAR_PROYECTO_HTML, data
        )

    return render(
        request,
        my_constants.CERRAR_PROYECTO_HTML, data
    )


def gantt(request):
    return render(
        request,
        "procesos/gantt.html",
    )


"""
////////////////////////////////////////////////////////////////////////////
    METODOS DE INFORMES
/////////////////////////////////////////////////////////////////////////////
"""


@validar_proyecto
def generar_informe_identificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_identificar(proyecto)

    zip_file = open(reporte, 'rb')
    response = HttpResponse(zip_file, content_type=my_constants.FORMAT_EXCEL)
    response['Content-Disposition'] = my_constants.ADJUNTO_EXCEL % reporte
    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print(my_constants.NO_EXIST_EXCEL)
    return response


@validar_proyecto
def generar_informe_planificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_planificar(proyecto)

    zip_file = open(reporte, 'rb')
    response = HttpResponse(zip_file, content_type=my_constants.FORMAT_EXCEL)
    response['Content-Disposition'] = my_constants.ADJUNTO_EXCEL % reporte
    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print(my_constants.NO_EXIST_EXCEL)
    return response


@validar_proyecto
def generar_informe_evaluar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_evaluar(proyecto)

    zip_file = open(reporte, 'rb')
    response = HttpResponse(zip_file, content_type=my_constants.FORMAT_EXCEL)
    response['Content-Disposition'] = my_constants.ADJUNTO_EXCEL % reporte
    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print(my_constants.NO_EXIST_EXCEL)
    return response


@validar_proyecto
def generar_informe_planificar_respuesta(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_planificar_respuesta(proyecto)

    zip_file = open(reporte, 'rb')
    response = HttpResponse(zip_file, content_type=my_constants.FORMAT_EXCEL)
    response['Content-Disposition'] = my_constants.ADJUNTO_EXCEL % reporte

    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print(my_constants.NO_EXIST_EXCEL, reporte)
    return response


@validar_proyecto
def generar_informe_controlar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_controlar_riesgos(proyecto)

    zip_file = open(reporte, 'rb')
    response = HttpResponse(zip_file, content_type=my_constants.FORMAT_EXCEL)
    response['Content-Disposition'] = my_constants.ADJUNTO_EXCEL % reporte

    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print(my_constants.NO_EXIST_EXCEL, reporte)
    return response


"""
////////////////////////////////////////////////////////////////////////////
    METODO PARA GENERAR REPORTES EN EXCEL
/////////////////////////////////////////////////////////////////////////////
"""


#######################################
## METODOS UTIL
#######################################
def get_fecha_actual():
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    return date_time


def manual(request):
    manual = "manual.pdf"
    zip_file = open(manual, 'rb')
    response = HttpResponse(zip_file, content_type="application/pdf")
    response['Content-Disposition'] = my_constants.ADJUNTO_EXCEL % manual
    return response
