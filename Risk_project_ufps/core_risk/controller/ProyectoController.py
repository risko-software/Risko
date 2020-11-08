from Risk_project_ufps.core_risk.dao.ProyectoDao import *
from Risk_project_ufps.core_risk.dao.ImpactoDao import *
from Risk_project_ufps.core_risk.dao.ProbabilidadDao import *
from Risk_project_ufps.core_risk.dao.ClasificacionRiesgoDao import *
from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgoDao import *
from Risk_project_ufps.core_risk.dao.TareaDao import *

from Risk_project_ufps.core_risk.dto.models import *

import datetime



class ProyectoController:

    def registrar_proyecto(self, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio, gerente, sector):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.registrar_proyecto(nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio,
                                               gerente, sector)

    def listar_proyectos(self, id):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.listar_proyectos(id)

    def obtener_proyecto(self, id):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.obtener_proyecto(id)

    def obtener_proyecto_linea_base(self, proyecto_id):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.obtener_proyecto_linea_base(proyecto_id)

    def eliminar_proyecto(self, proyecto):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.eliminar_proyecto(proyecto)

    

    def validar_proyecto(self, nombre, gerente_id):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.validar_proyecto(nombre, gerente_id)

    def editar_proyecto(self, proyecto, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio, sector):
        proyecto_dao = ProyectoDao()
        return proyecto_dao.editar_proyecto(proyecto, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio,
                                            sector)

    def has_actividades(self, proyecto_id):
        proyecto_dao = ProyectoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        return proyecto_dao.has_actividades(proyecto)

    def obtener_impactos_by_proyecto_id(self, proyecto_id):
        impacto_dao = ImpactoDao()
        proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()

        p_h_r = proyecto_has_riesgo_dao.get_all_by_proyecto_id(proyecto_id)
        proyecto = Proyecto(proyecto_id=proyecto_id)

        impactos = impacto_dao.listar_impactos_by_proyecto(proyecto)
        return self.set_has_riesgo_impactos(p_h_r, impactos)


    def obtener_probabilidades_by_proyecto_id(self, proyecto_id):
        probabilidad_dao = ProbabilidadDao()
        proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()

        p_h_r = proyecto_has_riesgo_dao.get_all_by_proyecto_id(proyecto_id)
        proyecto = Proyecto(proyecto_id=proyecto_id)

        probabilidades = probabilidad_dao.listar_probabilidades_by_proyecto(proyecto)
        return self.set_has_riesgo_probabilidades(p_h_r, probabilidades)

    def obtener_clasificaciones_riesgo_by_proyecto_id(self, proyecto_id):
        clasificacion_riesgo_dao = ClasificacionRiesgoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        return clasificacion_riesgo_dao.listar_clasificaciones_by_proyecto(proyecto)

    def actualizar_impactos_by_proyecto_id(self, impactos, proyecto_id):
        impacto_dao = ImpactoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        impactos_aux = impacto_dao.listar_impactos_by_proyecto(proyecto)
        for impacto_aux in impactos_aux:
            flag = False
            for impacto in impactos:
                if impacto['id'] is not None and impacto_aux.impacto_id == int(impacto['id']):
                    impacto_aux.impacto_categoria = impacto['nombre']
                    impacto_aux.impacto_valor = int(impacto['valor'])
                    impacto_aux.save()
                    flag = True
                    break
            if not flag:
                impacto_aux.delete()
        for impacto in impactos:
            if impacto['id'] is None:
                impacto_dao.crear_impacto(impacto["nombre"], impacto["valor"], proyecto)

    def actualizar_probabilidades_by_proyecto_id(self, probabilidades, proyecto_id):
        probabilidad_dao = ProbabilidadDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        probabilidades_aux = probabilidad_dao.listar_probabilidades_by_proyecto(proyecto)
        for probabilidad_aux in probabilidades_aux:
            flag = False
            for probabilidad in probabilidades:
                if probabilidad['id'] is not None and probabilidad_aux.propabilidad_id == int(probabilidad['id']):
                    probabilidad_aux.propabilidad_categoria = probabilidad['nombre']
                    probabilidad_aux.propabilidad_valor = int(probabilidad['valor'])
                    probabilidad_aux.save()
                    flag = True
                    break
            if not flag:
                probabilidad_aux.delete()
        for probabilidad in probabilidades:
            if probabilidad['id'] is None:
                probabilidad_dao.crear_probabilidad(probabilidad["nombre"], probabilidad["valor"], proyecto)

    def actualizar_clasificacion_riesgo_by_proyecto_id(self, clasificaciones, proyecto_id):
        clasificacion_riesgo_dao = ClasificacionRiesgoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        result = clasificacion_riesgo_dao.eliminar_clasificaciones_by_proyecto(proyecto)
        if result:
            for clasificacion in clasificaciones:
                clasificacion_riesgo_dao.crear_clasificacion(
                    clasificacion["nombre"],
                    clasificacion["color"],
                    clasificacion["valor_min"],
                    clasificacion["valor_max"],
                    proyecto
                )

    def obtener_impactos_parseados_by_proyecto_id(self, proyecto_id):
        impacto_dao = ImpactoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        impactos = impacto_dao.listar_impactos_by_proyecto(proyecto)
        return self.parsear_impactos(impactos)

    def obtener_impactos_parseados_by_proyecto_id_linea(self, proyecto_id, linea_base):
        impacto_dao = ImpactoDao()
        proyecto = Proyecto.objects.using('base').get(proyecto_id=proyecto_id, proyecto_linea_base=linea_base)
        impactos = impacto_dao.listar_impactos_by_proyecto_linea(proyecto, linea_base)
        return self.parsear_impactos(impactos)

    def obtener_probabilidades_parseados_by_proyecto_id(self, proyecto_id):
        probabilidad_dao = ProbabilidadDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        r = probabilidad_dao.listar_probabilidades_by_proyecto(proyecto)
        return self.parsear_probabilidades(r)

    def obtener_probabilidades_parseados_by_proyecto_id_linea(self, proyecto_id, linea_base):
        probabilidad_dao = ProbabilidadDao()
        proyecto = Proyecto.objects.using('base').get(proyecto_id=proyecto_id, proyecto_linea_base=linea_base)
        r = probabilidad_dao.listar_probabilidades_by_proyecto_linea(proyecto, linea_base)
        return self.parsear_probabilidades(r)

    def obtener_rangos_parseados_by_proyecto_id(self, proyecto_id):
        clasificacion_riesgo_dao = ClasificacionRiesgoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        rangos = clasificacion_riesgo_dao.listar_clasificaciones_by_proyecto(proyecto)
        return self.parsear_rangos(rangos)

    def obtener_rangos_parseados_by_proyecto_id_linea(self, proyecto_id, linea_base):
        clasificacion_riesgo_dao = ClasificacionRiesgoDao()
        proyecto = Proyecto.objects.using('base').get(proyecto_id=proyecto_id, proyecto_linea_base=linea_base)
        rangos = clasificacion_riesgo_dao.listar_clasificaciones_by_proyecto_linea(proyecto, linea_base)
        return self.parsear_rangos(rangos)

    def parsear_impactos(self, impactos: "list of Impacto"):
        aux = []
        aux_2 = []
        for impacto in impactos:
            aux.append({
                "id": impacto.impacto_id,
                "nombre": impacto.impacto_categoria,
                "escala": impacto.impacto_valor
            })
            aux_2.append(impacto.impacto_valor)
        return {"impactos": aux, "impactos_valores": aux_2}

    def parsear_probabilidades(self, probabilidades: "list of Propabilidad"):
        aux = []
        aux_2 = []
        for probabilidad in probabilidades:
            aux.append({
                "id": probabilidad.propabilidad_id,
                "nombre": probabilidad.propabilidad_categoria,
                "escala": probabilidad.propabilidad_valor
            })
            aux_2.append(probabilidad.propabilidad_valor)
        return {"probabilidades": aux, "probabilidades_valores": aux_2}

    def parsear_rangos(self, rangos: "List of ClasificacionRiesgo"):
        x = 0
        aux = []
        for rango in rangos:
            aux.append({
                "posicion": x,
                "nombre": rango.clasificacion_riesgo_nombre,
                "rango": [rango.clasificacion_riesgo_min, rango.clasificacion_riesgo_max],
                "color": rango.clasificacion_color
            })
        return aux

    def actualizar_valores_riesgo_proyecto(self, valores, proyecto_id):
        p_h_r = ProyectoHasRiesgoDao()
        for key in valores:
            p_h_r_aux = p_h_r.get_by_riesgo_and_proyecto(Proyecto(proyecto_id=proyecto_id),
                                                         Riesgo(riesgo_id=valores[key]['riesgo']))
            if 'impacto' in key:
                p_h_r_aux.impacto_id = valores[key]['id']
            elif 'probabilidad' in key:
                p_h_r_aux.propabilidad_id = valores[key]['id']
            p_h_r_aux.save()

    def crear_linea_base(self, gerente_id, proyecto_id):
        proyecto_dao = ProyectoDao()
        proyecto = proyecto_dao.obtener_proyecto(proyecto_id)
        return proyecto_dao.crear_linea_base(gerente_id, proyecto)

    def actualizar_gantt(self, proyecto_id, gantt):
        tarea_dao = TareaDao()
        proyecto_dao = ProyectoDao()
        proyecto = proyecto_dao.obtener_proyecto(proyecto_id)
        flag = False
        riesgos = gantt['children']
        for riesgo in riesgos:
            actividades = riesgo['children']
            for actividad in actividades:
                tareas = actividad['children']
                for tarea in tareas:
                    fecha_inicio_real = datetime.datetime.strptime(tarea['start_date_real'],'%Y-%m-%dT%H:%M:%S')
                    fecha_fin_real = fecha_inicio_real + datetime.timedelta(days=int(tarea['duration_real']))
                    tarea_aux = Tarea(
                        tarea_id=tarea['tarea_id'],
                        fecha_inicio_real=fecha_inicio_real,
                        fecha_fin_real=fecha_fin_real,
                        duracion_real=tarea['duration_real'],
                        tarea_estado=self.get_id_estado_text(tarea['estado_text']),
                        tarea_observacion=tarea['observacion']
                    )
                    flag = tarea_dao.actualizar_tarea_bd(tarea_aux)
                    flag = tarea_dao.actualizar_tarea_base(tarea_aux, proyecto)
        return flag

    def get_datetime(self):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d")
        # print("date and time:",date_time)
        return date_time


    def get_lineas_base(self, proyecto_id):        
        proyecto_dao = ProyectoDao()        
        return proyecto_dao.get_lineas_base(proyecto_id)

    def cerrar_proyecto(self, proyecto, fecha):        
        proyecto_dao = ProyectoDao()        
        return proyecto_dao.cerrar_proyecto(proyecto, fecha)

    def get_id_estado_text(self, estado):
        aux = ''
        if estado == 'No iniciado':
            aux = 1
        elif estado == 'Iniciado':
            aux = 2
        elif estado == 'Completado':
            aux = 3
        return aux

    def set_has_riesgo_impactos(self, p_h_r, impactos):
        for impacto in impactos:
            for aux in p_h_r:
                if aux.impacto.impacto_id == impacto.impacto_id:
                    impacto.has_riesgo += 1
        return impactos

    def set_has_riesgo_probabilidades(self, p_h_r, probabilidades):
        for probabilidad in probabilidades:
            for aux in p_h_r:
                if aux.propabilidad.propabilidad_id == probabilidad.propabilidad_id:
                    probabilidad.has_riesgo += 1
        return probabilidades




