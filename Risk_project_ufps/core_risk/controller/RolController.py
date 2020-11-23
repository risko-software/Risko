from Risk_project_ufps.core_risk.dao.RolDao import *
from Risk_project_ufps.core_risk.dto.models import *
from django.forms.models import model_to_dict

class RolController:

	def registrar_rol(self, nombre, descripcion, gerente):
		rol_dao = RolDao()
		return rol_dao.registrar_rol(nombre, descripcion, gerente)

	def listar_roles(self, gerente):
		rol_dao = RolDao()
		return rol_dao.listar_roles(gerente)

	def editar_rol(self, rol, nombre, descripcion):
		rol_dao = RolDao() 
		return rol_dao.editar_rol(rol, nombre, descripcion)
	
	def get_rol_by_id(self, rol_id):
		rol_dao = RolDao()
		return rol_dao.get_rol_by_id(rol_id)

	def eliminar_rol(self, rol):
		rol_dao = RolDao()
		return rol_dao.eliminar_rol(rol)
	
	def lista_roles_utilizados(self, gerente_id):
		rol_dao = RolDao()
		return rol_dao.lista_roles_utilizados(gerente_id)

	def convert_to_dict(self, roles):
		aux = []
		for rol in roles:
			aux.append(model_to_dict(rol))
		return aux
		

