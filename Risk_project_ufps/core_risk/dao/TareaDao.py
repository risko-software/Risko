from Risk_project_ufps.core_risk.dto.models import Tarea
from datetime import date
from datetime import datetime
from contextlib import closing
from Risk_project_ufps.core_risk.util.cadena import limpiar_descripcion
from django.db import connections


class TareaDao:

    def registrar_tarea(self, proyecto_riesgo_respuesta, nombre, descripcion, fecha_inicio, fecha_fin,
                        fecha_inicio_real, fecha_fin_real):
        tarea = Tarea(
            proyecto_has_riesgo_id=proyecto_riesgo_respuesta.proyecto_has_id,
            riesgo_has_respuesta_id=proyecto_riesgo_respuesta.respuesta_has_id,
            tarea_nombre=nombre,
            tarea_descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fecha_inicio_real=fecha_inicio_real,
            fecha_fin_real=fecha_fin_real,
            tarea_estado=1,
            tarea_observacion=''
        )
        try:
            tarea.save()
        except Exception as e:
            print(e)
        return tarea

    def get_tarea_by_id(self, id):
        tarea = None
        try:
            tarea = Tarea.objects.get(tarea_id=id)
        except Exception as e:
            print(e)
        return tarea

    def listar_tareas(self, proyecto):
        tareas = {}
        try:
            sql = "SELECT t.tarea_id, t.tarea_nombre, t.tarea_descripcion, rp.riesgo_id FROM tarea t " \
                  "INNER JOIN proyecto_has_riesgo_respuesta pr " \
                  "ON t.proyecto_has_riesgo_id=pr.proyecto_has_id " \
                  "AND t.riesgo_has_respuesta_id=pr.respuesta_has_id " \
                  "INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id " \
                  "WHERE rp.proyecto_id = %s"
            tareas = Tarea.objects.raw(sql, [proyecto.proyecto_id])
        except Exception as e:
            print(e)
        return tareas

    def validar_tarea(self, nombre, respuesta_id, proyecto):
        tarea = None
        try:
            sql = "SELECT t.tarea_id, t.tarea_nombre, t.tarea_descripcion, rp.riesgo_id FROM tarea t " \
                  "INNER JOIN proyecto_has_riesgo_respuesta pr " \
                  "ON t.proyecto_has_riesgo_id=pr.proyecto_has_id " \
                  "AND t.riesgo_has_respuesta_id=pr.respuesta_has_id " \
                  "INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id " \
                  "INNER JOIN riesgo_has_respuesta rr ON pr.respuesta_has_id = rr.riesgo_has_respuesta_id" \
                  "WHERE rp.proyecto_id = %s AND t.tarea_nombre = %s AND rr.respuesta_id = %s"
            tarea = Tarea.objects.raw(sql, [proyecto.proyecto_id, nombre, respuesta_id])
        except Exception as e:
            print(e)
        return tarea

    def listar_tareas_linea(self, proyecto, linea_base):
        tareas = {}
        try:
            sql = "SELECT t.tarea_id, t.tarea_nombre, t.tarea_descripcion, rp.riesgo_id FROM tarea t " \
                  "INNER JOIN proyecto_has_riesgo_respuesta pr " \
                  "ON t.proyecto_has_riesgo_id=pr.proyecto_has_id " \
                  "AND t.riesgo_has_respuesta_id=pr.respuesta_has_id " \
                  "INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id " \
                  "WHERE rp.proyecto_id = %s AND t.proyecto_linea_base = %s AND pr.proyecto_linea_base = %s AND rp.proyecto_linea_base = %s"
            tareas = Tarea.objects.using('base').raw(sql, [proyecto.proyecto_id, linea_base, linea_base, linea_base])
        except Exception as e:
            print(e)
        return tareas

    def listar_tareas_no_iniciadas(self, proyecto):
        tareas = {}
        try:
            sql = "SELECT * FROM tarea t " \
                  "WHERE t.proyecto_id = %s AND t.proyecto_linea_base = %s AND NOT t.tarea_estado = %s "

            tareas = Tarea.objects.using('base').raw(sql, [proyecto.proyecto_id, proyecto.proyecto_linea_base, 3])

        except Exception as e:
            print(e)
        return tareas

    def listar_tareas_base(self, proyecto):
        tareas = {}
        try:
            sql = "SELECT t.`tarea_id`, " \
                  "t.`proyecto_linea_base`, " \
                  "t.`tarea_nombre`, " \
                  "t.`tarea_descripcion`, " \
                  "t.`proyecto_has_riesgo_id`, " \
                  "t.`riesgo_has_respuesta_id`, " \
                  "t.`fecha_inicio`, " \
                  "t.`duracion`, " \
                  "t.`fecha_fin`, " \
                  "t.`fecha_inicio_real`, " \
                  "t.`duracion_real`, " \
                  "t.`fecha_fin_real`, " \
                  "t.`tarea_observacion`, " \
                  "t.`tarea_estado`, " \
                  "t.`proyecto_id`, " \
                  "rp.riesgo_id " \
                  "FROM tarea t " \
                  "INNER JOIN proyecto_has_riesgo_respuesta pr " \
                  "ON t.proyecto_has_riesgo_id=pr.proyecto_has_id " \
                  "AND t.riesgo_has_respuesta_id=pr.respuesta_has_id " \
                  "INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id " \
                  "WHERE rp.proyecto_id = %s " \
                  "AND rp.proyecto_linea_base = %s " \
                  "AND pr.proyecto_linea_base = %s " \
                  "AND t.proyecto_linea_base = %s "
            tareas = Tarea.objects.using('base').raw(sql, [proyecto.proyecto_id,
                                                           proyecto.proyecto_linea_base,
                                                           proyecto.proyecto_linea_base,
                                                           proyecto.proyecto_linea_base, ])
        except Tarea.DoesNotExist as e:
            print(e)
        return tareas

    def listar_tareas_with_recursos(self, proyecto):
        tareas = {}
        try:
            sql = "SELECT t.tarea_id, t.tarea_nombre, t.tarea_descripcion, rp.riesgo_id FROM tarea t " \
                  "INNER JOIN proyecto_has_riesgo_respuesta pr " \
                  "ON t.proyecto_has_riesgo_id=pr.proyecto_has_id " \
                  "AND t.riesgo_has_respuesta_id=pr.respuesta_has_id " \
                  "INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id " \
                  "WHERE rp.proyecto_id = %s"
            tareas = Tarea.objects.raw(sql, [proyecto.proyecto_id])
        except Exception as e:
            print(e)
            print("tareas")
        return tareas

    def eliminar_tarea(self, tarea):
        msg = "No se elimino la tarea"
        tarea_eliminar = tarea
        try:
            tarea_eliminar.delete()
            msg = "Tarea eliminada de forma exitosa."
        except Exception as e:
            print(e)
        return msg

    def editar_tarea(self, tarea, nombre, descripcion, fecha_inicio, fecha_fin):
        tarea_editar = tarea
        tarea_editar.tarea_nombre = nombre
        tarea_editar.tarea_descripcion = descripcion
        tarea_editar.fecha_inicio = fecha_inicio
        tarea_editar.fecha_fin = fecha_fin
        tarea_editar.fecha_inicio_real = fecha_inicio
        tarea_editar.fecha_fin_real = fecha_fin
        try:
            tarea_editar.save()
        except Exception as e:
            print(e)
        return tarea_editar

    def actualizar_tarea_base(self, tarea_aux, proyecto):
        flag = False
        try:
            with closing(connections['base'].cursor()) as cursor:
                sql = 'UPDATE tarea ' \
                      'SET fecha_inicio_real = %s, ' \
                      'fecha_fin_real = %s, ' \
                      'tarea_estado = %s, ' \
                      'tarea_observacion = %s, ' \
                      'duracion_real = %s ' \
                      'WHERE tarea_id = %s ' \
                      'AND proyecto_id = %s ' \
                      'AND proyecto_linea_base = %s; '
                cursor.execute(
                    sql,
                    [tarea_aux.fecha_inicio_real,
                     tarea_aux.fecha_fin_real,
                     tarea_aux.tarea_estado,
                     tarea_aux.tarea_observacion,
                     tarea_aux.duracion_real,
                     tarea_aux.tarea_id,
                     proyecto.proyecto_id,
                     proyecto.proyecto_linea_base,
                     ],
                )
                #print("WWWWWWw",cursor._last_executed)
                flag = True
        except Exception as e:
            print(e)
        return flag

    def actualizar_tarea_bd(self, tarea):
        """
        Actualiza los campos de fechas usados en controlar

        :param tarea: Tarea
        :rtype: Tarea
        """
        try:
            tarea_editar = Tarea.objects.get(tarea_id=tarea.tarea_id)
            tarea_editar.fecha_inicio_real = tarea.fecha_inicio_real
            tarea_editar.fecha_fin_real = tarea.fecha_fin_real
            tarea_editar.duracion_real = tarea.duracion_real
            tarea_editar.tarea_estado = tarea.tarea_estado
            tarea_editar.tarea_descripcion = tarea.tarea_descripcion
            tarea_editar.tarea_observacion = tarea.tarea_observacion
            tarea_editar.save()
        except Tarea.DoesNotExist:
            tarea_editar = None
        return tarea_editar







