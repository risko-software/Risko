from Risk_project_ufps.core_risk.dto.models import Proyecto
from Risk_project_ufps.core_risk.dto.models import Actividad
from Risk_project_ufps.core_risk.util.cadena import limpiar_descripcion
from contextlib import closing
from django.db import connections

class ProyectoDao:

    def registrar_proyecto(self, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio, gerente, sector):
        proyecto = None
        try:
            proyecto = Proyecto.objects.create(
                proyecto_nombre=nombre,
                proyecto_objetivo=limpiar_descripcion(objetivo),
                proyecto_alcance=limpiar_descripcion(alcance),
                proyecto_descripcion=limpiar_descripcion(descripcion),
                proyecto_presupuesto=presupuesto,
                proyecto_fecha_inicio=fecha_inicio,
                gerente=gerente,
                sector=sector,
                proyecto_rbs_status=0,
                proyecto_linea_base=0)
        except Exception as e:
            print(e)
        return proyecto

    def obtener_proyecto(self, id):
        proyecto = None
        try:
            proyecto = Proyecto.objects.get(proyecto_id=id)
        except Exception as e:
            print(e)
        return proyecto


    def obtener_proyecto_linea_base(self, proyecto_id):
        proyecto = None
        try:
            proyecto = Proyecto.objects.using('base').get(proyecto_id=proyecto_id)
        except Proyecto.DoesNotExist as e:
            print(e)
        return proyecto



    def validar_proyecto(self, nombre, gerente_id):
        proyecto = None
        try:
            proyecto = Proyecto.objects.get(proyecto_nombre=nombre, gerente_id=gerente_id)
        except Exception as e:
            print(e)
        return proyecto

    def eliminar_proyecto(self, proyecto):
        flag = False
        try:
            proyecto.gerente_id = None
            proyecto.save()
            flag = True
        except Exception as e:
            print(e)
        return flag

    def editar_proyecto(self, proyecto, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio, sector):
        msg = "No se actualizo la información del proyecto."
        try:
            proyecto.proyecto_nombre = nombre
            proyecto.proyecto_objetivo = limpiar_descripcion(objetivo)
            proyecto.proyecto_alcance = limpiar_descripcion(alcance)
            proyecto.proyecto_descripcion = limpiar_descripcion(descripcion)
            proyecto.proyecto_presupuesto = presupuesto
            proyecto.proyecto_fecha_inicio = fecha_inicio
            proyecto.sector = sector
            proyecto.save()
            msg = "Se actualizo la información del proyecto de forma exitosamente."
        except Exception as e:
            print(e)
        return msg

    def cerrar_proyecto(self, proyecto, fecha):
        try:
            proyecto.proyecto_fin_status = 1
            proyecto.proyecto_fecha_finl = fecha          
            proyecto.save()
        except Exception as e:
            print(e)
        return proyecto

    def listar_proyectos(self, id):
        proyectos = {}
        try:
            proyectos = Proyecto.objects.filter(gerente_id=id).order_by('-proyecto_fecha_inicio')
        except Exception as e:
            print(e)
        return proyectos

    def get_lineas_base(self, proyecto_id):
        proyectos = {}
        try:
          sql = "SELECT * FROM proyecto p " \
                "WHERE p.proyecto_id = %s ORDER BY p.proyecto_linea_base "
          proyectos = Proyecto.objects.using('base').raw(sql, [proyecto_id])
        except Exception as e:
          print(e)
        return proyectos

    def has_actividades(self, proyecto):
        flag = False
        try:
            sql = "SELECT * FROM `actividad` WHERE `proyecto_id` = %s LIMIT 1"
            actividad = Actividad.objects.raw(sql, [proyecto.proyecto_id, ])
            if actividad:
                flag = True
        except Exception as e:
            print(e)
        return flag

    def crear_linea_base(self, gerente_id: int, proyecto):
        try:
            with closing(connections['riesgos'].cursor()) as cursor:
                cursor.callproc('crear_linea_base',
                                [gerente_id, proyecto.proyecto_id, proyecto.proyecto_linea_base + 1])
            flag = True
        except Exception as e:
            print(e)
            flag = False
        return flag

    def get_cantidad_proyectos(self):
        return Proyecto.objects.count()
