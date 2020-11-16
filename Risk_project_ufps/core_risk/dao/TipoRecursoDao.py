from Risk_project_ufps.core_risk.dto.models import TipoRecurso


class TipoRecursoDao:

    def registrar_tipo_recurso(self, nombre, descripcion, gerente):
        msg = "No se pudo registrar"
        tipo_recurso = TipoRecurso(
            tipo_recurso_nombre=nombre,
            tipo_recurso_descripcion=descripcion,
            gerente=gerente)
        try:
            tipo_recurso.save()
            msg = "Se registró un tipo de recurso exitosamente."
        except Exception as e:
            print(e)
        return msg

    def eliminar_tipo_recurso(self, tipo_recurso):
        msg = "no se elimino el tipo de recurso"
        try:
            tipo_recurso.delete()
            msg = "Se elimino un tipo de recurso de forma exitosa."
        except Exception as e:
            print(e)
        return msg

    def editar_tipo_recurso(self, tipo_recurso, nombre, descripcion):
        msg = "No se actualizo el tipo de recurso"
        try:
            tipo_recurso.tipo_recurso_nombre = nombre
            tipo_recurso.tipo_recurso_descripcion = descripcion
            tipo_recurso.save()
            msg = "Se actualizo la información de tipo de recurso de forma exitosa."
        except Exception as e:
            print(e)
        return msg

    def obtener_tipo_recurso(self, id):
        tipo_recurso = None
        try:
            tipo_recurso = TipoRecurso.objects.get(tipo_recurso_id=id)
        except Exception as e:
            print(e)
        return tipo_recurso

    def listar_tipos_recursos(self, id):
        tipo_recurso = {}
        try:
            tipo_recurso = TipoRecurso.objects.filter(gerente_id=id)
        except Exception as e:
            print(e)
        return tipo_recurso
