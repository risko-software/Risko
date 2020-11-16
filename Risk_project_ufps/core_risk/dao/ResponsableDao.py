from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgoDao import *
from Risk_project_ufps.core_risk.util.cadena import limpiar_descripcion
from Risk_project_ufps.core_risk.dto.models import Responsble


class ResponsableDao:

    def registrar_responsable(self, nombre, descripcion, proyecto, rol):
        msg = "No se pudo registrar el responsble."
        try:
            responsable = Responsble(
                responsble_nombre=nombre,
                responsble_descripcion=limpiar_descripcion(descripcion),
                proyecto_id=proyecto,
                rol_id=rol.rol_id
            )
            responsable.save()
            msg = "Se registro un miembro de equipo exitosamente."
        except Exception as e:
            print(e)
        return msg

    def listar_responsables(self, id):
        responsables = {}
        try:
            responsables = Responsble.objects.filter(proyecto_id=id)
        except Exception as e:
            print(e)
        return responsables

    def obtener_responsable(self, id):
        responsable = None
        try:
            responsable = Responsble.objects.get(responsable_id=id)
        except Responsble.DoesNotExist:
            responsable = Responsble()
        return responsable

    def editar_responsable(self, responsable, nombre, descripcion, rol):
        msg = "No se actualizo la informacion."
        try:
            responsable.responsble_nombre = nombre
            responsable.responsble_descripcion = limpiar_descripcion(descripcion)
            responsable.rol_id = rol.rol_id
            responsable.save()
            msg = "Se actualizo la información del miembro del equipo exitosamente."
        except Exception as e:
            print(e)
        return msg

    def eliminar_responsable(self, responsable):
        msg = "No se elimino responsable."
        try:
            responsable.delete()
            msg = "Se eliminó un miembro del equipo exitosamente."
        except Exception as e:
            print(e)
        return msg

    def eliminar_responsable_riesgo(self, responsable_id, riesgo_id, proyecto_id):
        proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()
        return proyecto_has_riesgo_dao.set_responsable_null(responsable_id, riesgo_id, proyecto_id)










