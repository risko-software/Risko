from Risk_project_ufps.core_risk.dao.ActividadDao import *
from Risk_project_ufps.core_risk.dao.RiesgoDao import *
from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgo_ActividadDao import *
from Risk_project_ufps.core_risk.dto.models import *

from django.forms.models import model_to_dict


class ActividadController:

    def listar_actividades_proyecto(self, proyecto_id):
        actividad_dao = ActividadDao()
        actividades = actividad_dao.listar_actividades_proyecto(proyecto_id)
        aux = []
        for actividad in actividades:
            actividad_aux = dict(
                actividad_id=actividad.actividad_id,
                actividad_orden=actividad.actividad_orden,
                actividad_uuid=actividad.actividad_uuid,
                actividad_nombre=actividad.actividad_nombre,
                actividad_level=actividad.actividad_level,
                actividad_wbs=actividad.actividad_wbs,
                actividad_fecha_inicio=actividad.actividad_fecha_inicio.strftime("%Y-%m-%d"),
                actividad_fecha_fin=actividad.actividad_fecha_fin.strftime("%Y-%m-%d"),
                duracion=actividad.duracion
            )
            aux.append(actividad_aux)
        return aux

    def obtener_actividad(self, actividad_id):
        actividad_dao = ActividadDao()
        return actividad_dao.obtener_actividad(actividad_id)

    def registrar_actividad_riesgo(self, proyecto_riesgo, actividad):
        actividad_dao = ProyectoHasRiesgo_ActividadDao()
        return actividad_dao.registrar_actividad_riesgo(proyecto_riesgo, actividad)

    def listar_actividades_riesgo(self, proyecto_id):
        actividad_dao = ProyectoHasRiesgo_ActividadDao()
        actividades = actividad_dao.listar_actividades_riesgo(proyecto_id)
        aux = {}
        for actividad in actividades:
            key = "riesgo_" + str(actividad.riesgo_id)
            riesgo_aux = aux.get(key)
            if (riesgo_aux == None):
                aux[key] = []

            aux[key].append({
                "actividad_id": actividad.actividad_id,
                "actividad_nombre": actividad.actividad_nombre,
                "actividad_level": actividad.actividad_level,
                "actividad_fecha_inicio": actividad.actividad_fecha_inicio.strftime("%Y-%m-%d"),
                "actividad_fecha_fin": actividad.actividad_fecha_fin.strftime("%Y-%m-%d")
            })
        return aux

    def validar_actividad(self, proyecto_riesgo, actividad_id):
        actividad_dao = ProyectoHasRiesgo_ActividadDao()
        return actividad_dao.validar_actividad(proyecto_riesgo, actividad_id)

    def desasociar_actividad_riesgo(self, proyecto_id, riesgo_id, actividad_id):
        p_h_r_a = ProyectoHasRiesgo_ActividadDao()
        p_h_r = ProyectoHasRiesgoDao()

        proyecto = Proyecto(proyecto_id=proyecto_id)
        riesgo = Riesgo(riesgo_id=riesgo_id)
        actividad = Actividad(actividad_id=actividad_id)

        proyecto_has_riesgo = p_h_r.get_by_riesgo_and_proyecto_2(riesgo, proyecto)

        return p_h_r_a.desasociar_actividad_riesgo(proyecto_has_riesgo, actividad)

    def actualizar_actividades_proyecto(self, actividades, proyecto_id):
        proyecto_has_actividad = ProyectoHasRiesgo_ActividadDao()
        actividad_dao = ActividadDao()

        proyecto = Proyecto(proyecto_id=proyecto_id)

        actividades_eliminar = actividad_dao.listar_actividades_sin_uso(proyecto)
        actividad_dao.eliminar_actividades(actividades_eliminar)

        actividades_proyecto = proyecto_has_actividad.listar_actividades_riesgo(proyecto_id)
        list_uid = self.get_uid_from_actividades(actividades_proyecto)
        actividades_pendientes = []
        for actividad in actividades:
            print("DOS", actividad["uid"])
            actividad_old = list_uid.get('a_' + str(actividad["uid"]))
            actividad_new = self.construir_actividad(actividad, proyecto)
            if actividad_old:
                actividad_dao.actualizar_actividad_2(actividad_old, actividad_new)
            else:
                actividades_pendientes.append(actividad_new)
        for actividad in actividades_pendientes:
            actividad.save()

    def get_uid_from_actividades(self, actividades):
        aux = {}
        for actividad in actividades:
            print("UNOS", actividad.actividad_uuid)
            aux['a_' + str(actividad.actividad_uuid)] = actividad
        return aux

    def construir_actividad(self, actividad, proyecto):
        return Actividad(
            actividad_id=actividad["id"],
            actividad_orden=actividad["orden"],
            actividad_uuid=actividad["uid"],
            actividad_nombre=actividad["name"],
            actividad_level=actividad["level"],
            actividad_wbs=actividad["WBS"],
            proyecto=proyecto,
            actividad_fecha_inicio=actividad["start"],
            actividad_fecha_fin=actividad["end"],
            duracion=actividad["duration"]
        )
