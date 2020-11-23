from Risk_project_ufps.core_risk.dto.models import Rol
from Risk_project_ufps.core_risk.util.cadena import limpiar_descripcion


class RolDao:

    def registrar_rol(self, nombre, descripcion, gerente):
        rol = Rol(
            rol_nombre=nombre,
            rol_descripcion=limpiar_descripcion(descripcion),
            gerente=gerente)
        try:
            rol.save()
        except Exception as e:
            print(e)
        return rol

    def listar_roles(self, gerente):
        lista_roles = None
        try:
            lista_roles = Rol.objects.filter(gerente_id=gerente.gerente_id)
        except Exception as e:
            print(e)
        return lista_roles

    def editar_rol(self, rol, nombre, descripcion):
        try:
            rol.rol_nombre = limpiar_descripcion(nombre)
            rol.rol_descripcion = limpiar_descripcion(descripcion)
            rol.save()
        except Exception as e:
            print(e)
        return rol

    def get_rol_by_id(self, rol_id):
        rol = None
        try:
            rol = Rol.objects.get(rol_id=rol_id)
        except Exception as e:
            print(e)
        return rol

    def eliminar_rol(self, rol):
        flag = False
        try:
            rol.delete()
            flag = True
        except Exception as e:
            print(e)
        return flag

    def lista_roles_utilizados(self, gerente_id):
        lista_roles = None
        try:
            sql = 'SELECT r.rol_id, r.rol_nombre, r.rol_descripcion, r.gerente_id, r.proyecto_linea_base '\
                  'FROM rol r '\
                  'INNER JOIN responsble res '\
                  'ON r.rol_id = res.rol_id '\
                  'WHERE r.gerente_id = %s'
            lista_roles = Rol.objects.raw(sql, [gerente_id,])
        except Exception as e:
            print(e)
        return lista_roles        
