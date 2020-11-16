from Risk_project_ufps.core_risk.dto.models import Recurso


class RecursoDao:

    def registrar_recurso(self, proyecto, nombre, costo, tipo_recurso):
        msg = "No se registro el recurso"
        try:
            recurso = Recurso(recurso_nombre=nombre,
                              recurso_costo=costo,
                              tipo_recurso_id=tipo_recurso,
                              proyecto=proyecto
                              )
            recurso.save()
            msg = "Se registro un recurso exitosamente."
        except Exception as e:
            print(e)
        return msg

    def listar_recursos_linea(self, id, linea_base):
        recursos = {}
        try:
            recursos = Recurso.objects.using('base').filter(proyecto_id=id, proyecto_linea_base=linea_base)
        except Exception as e:
            print(e)
        return recursos

    def obtener_recurso(self, id):
        recurso = {}
        try:
            recurso = Recurso.objects.get(recurso_id=id)
        except Exception as e:
            print(e)
        return recurso

    def listar_recursos(self, id):
        recursos = {}
        try:
            recursos = Recurso.objects.filter(proyecto_id=id)
        except Exception as e:
            print(e)
        return recursos

    def eliminar_recurso(self, recurso):
        msg = "No se elimino el recurso."
        try:
            recurso.delete()
            msg = "Se eliminó recurso exitosamente."
        except Exception as e:
            print(e)
        return msg

    def editar_recurso(self, recurso, nombre, costo):
        msg = "No se actualizó la información del recurso."
        try:
            recurso.recurso_nombre = nombre
            recurso.recurso_costo = costo
            recurso.save()
            msg = "Se actualizó la información del recurso exitosamente."
        except Exception as e:
            print(e)
        return msg

    def listar_recursos_tareas_linea(self, proyecto, linea_base):
        recursos = {}
        try:
            sql = "SELECT * FROM recurso r INNER JOIN tarea_has_recurso tr ON r.recurso_id=tr.recurso_id INNER JOIN tarea t ON tr.tarea_id = t.tarea_id INNER JOIN proyecto_has_riesgo_respuesta pr ON t.proyecto_has_riesgo_id=pr.proyecto_has_id AND t.riesgo_has_respuesta_id=pr.respuesta_has_id INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id WHERE rp.proyecto_id = %s AND r.proyecto_linea_base = %s AND tr.proyecto_linea_base = %s AND t.proyecto_linea_base = %s AND pr.proyecto_linea_base = %s AND rp.proyecto_linea_base = %s"
            recursos = Recurso.objects.using('base').raw(sql, [proyecto.proyecto_id, linea_base, linea_base, linea_base,
                                                               linea_base, linea_base])
        except Exception as e:
            print(e)
        return recursos

    def listar_recursos_tareas(self, proyecto):
        recursos = {}
        try:
            sql = "SELECT * FROM recurso r INNER JOIN tarea_has_recurso tr ON r.recurso_id=tr.recurso_id INNER JOIN tarea t ON tr.tarea_id = t.tarea_id INNER JOIN proyecto_has_riesgo_respuesta pr ON t.proyecto_has_riesgo_id=pr.proyecto_has_id AND t.riesgo_has_respuesta_id=pr.respuesta_has_id INNER JOIN proyecto_has_riesgo rp ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id WHERE rp.proyecto_id = %s"
            recursos = Recurso.objects.raw(sql, [proyecto.proyecto_id])
        except Exception as e:
            print(e)
        return recursos

    def listar_recursos_tareas_base(self, proyecto):
        recursos = {}
        try:
            sql = "SELECT * FROM recurso r " \
                  "INNER JOIN tarea_has_recurso tr " \
                  "ON r.recurso_id=tr.recurso_id " \
                  "INNER JOIN tarea t " \
                  "ON tr.tarea_id = t.tarea_id " \
                  "INNER JOIN proyecto_has_riesgo_respuesta pr " \
                  "ON t.proyecto_has_riesgo_id=pr.proyecto_has_id " \
                  "AND t.riesgo_has_respuesta_id=pr.respuesta_has_id " \
                  "INNER JOIN proyecto_has_riesgo rp " \
                  "ON pr.proyecto_has_id = rp.proyecto_has_riesgo_id " \
                  "WHERE rp.proyecto_id = %s " \
                  "AND rp.proyecto_linea_base = %s " \
                  "AND pr.proyecto_linea_base = %s " \
                  "AND t.proyecto_linea_base = %s " \
                  "AND tr.proyecto_linea_base = %s " \
                  "AND r.proyecto_linea_base = %s "
            recursos = Recurso.objects.using('base').raw(sql, [proyecto.proyecto_id,
                                                               proyecto.proyecto_linea_base,
                                                               proyecto.proyecto_linea_base,
                                                               proyecto.proyecto_linea_base,
                                                               proyecto.proyecto_linea_base,
                                                               proyecto.proyecto_linea_base, ])
        except Exception as e:
            print(e)
        return recursos
