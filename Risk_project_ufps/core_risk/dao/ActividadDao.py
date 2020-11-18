from Risk_project_ufps.core_risk.dto.models import Actividad, Proyecto

from contextlib import closing

from django.db import connections


class ActividadDao:

    def listar_actividades_proyecto(self, proyecto_id):
        actividades = {}
        try:
            sql = "SELECT * FROM `actividad` WHERE `proyecto_id` = %s ORDER BY `actividad_orden`"
            actividades = Actividad.objects.raw(sql, [proyecto_id, ])
        except Exception as e:
            print(e)
        return actividades

    def obtener_actividad(self, actividad_id):
        actividad = None
        try:
            actividad = Actividad.objects.get(actividad_id=actividad_id)
        except Exception as e:
            print(e)
        return actividad

    def listar_actividades_sin_uso(self, proyecto):
        """
        Obtiene todas aquellas actividades que no se estan utilizando en ningun riesgo del proyecto
        @type proyecto: Proyecto
        """
        actividades = {}
        try:
            sql = "SELECT act.actividad_id " \
                  "FROM actividad act " \
                  "LEFT JOIN proyecto_has_riesgo_actividad pr " \
                  "ON act.actividad_id = pr.actividad_id " \
                  "WHERE pr.actividad_id IS NULL " \
                  "AND act.proyecto_id = %s"
            actividades = Actividad.objects.raw(sql, [proyecto.proyecto_id])
        except Exception as e:
            print(e)
        return actividades

    def eliminar_actividades(self, actividades):
        flag = False
        try:
            for actividad in actividades:
                actividad.delete()
            flag = True
        except Exception as e:
            print(e)
        return flag

    def actualizar_actividad(self, actividad_old, actividad_new):
        """
        Permite actualizar una actividad utilizando la informacion de otra actividad
        @param actividad_old: Actividad
        @param actividad_new: Actividad
        @return: bool
        """
        flag = False
        try:
            actividad_old.actividad_id = actividad_new.actividad_id
            actividad_old.actividad_orden = actividad_new.actividad_orden,
            actividad_old.actividad_uuid = actividad_new.actividad_uuid,
            actividad_old.actividad_nombre = actividad_new.actividad_nombre,
            actividad_old.actividad_level = actividad_new.actividad_level,
            actividad_old.actividad_wbs = actividad_new.actividad_wbs,
            actividad_old.proyecto = actividad_new.proyecto,
            actividad_old.actividad_fecha_inicio = actividad_new.actividad_fecha_inicio,
            actividad_old.actividad_fecha_fin = actividad_new.actividad_fecha_fin,
            actividad_old.duracion = actividad_new.duracion
            actividad_old.save()
            flag = True
        except Exception as e:
            print(e)
        return flag

    def actualizar_actividad_2(self, actividad_old, actividad_new):
        with closing(connections['riesgos'].cursor()) as cursor:
            sql = 'UPDATE `actividad` ' \
                  'SET `actividad_id`= %s,' \
                  '`actividad_orden`= %s,' \
                  '`actividad_uuid`= %s,' \
                  '`actividad_nombre`= %s,' \
                  '`actividad_level`= %s,' \
                  '`actividad_wbs`= %s,' \
                  '`proyecto_id`= %s,' \
                  '`proyecto_linea_base`= %s,' \
                  '`actividad_fecha_inicio`= %s,' \
                  '`actividad_fecha_fin`= %s,' \
                  '`duracion`= %s ' \
                  'WHERE `actividad_uuid`= %s ' \
                  'AND `actividad_id`= %s '
            cursor.execute(
                sql,
                (actividad_new.actividad_id, actividad_new.actividad_orden, actividad_new.actividad_uuid,
                 actividad_new.actividad_nombre, actividad_new.actividad_level, actividad_new.actividad_wbs,
                 actividad_new.proyecto.proyecto_id, actividad_old.proyecto_linea_base,
                 actividad_new.actividad_fecha_inicio,
                 actividad_new.actividad_fecha_fin, actividad_new.duracion, actividad_old.actividad_uuid,
                 actividad_old.actividad_id)
            )
