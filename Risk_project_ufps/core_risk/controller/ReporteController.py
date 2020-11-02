from Risk_project_ufps.core_risk.dao.RiesgoDao import *
from Risk_project_ufps.core_risk.dao.ResponsableDao import *
from Risk_project_ufps.core_risk.dao.ImpactoDao import *
from Risk_project_ufps.core_risk.dao.ProbabilidadDao import *
from Risk_project_ufps.core_risk.dao.ClasificacionRiesgoDao import *

from Risk_project_ufps.core_risk.controller.RiesgoController import *
from Risk_project_ufps.core_risk.controller.RespuestaController import *
from Risk_project_ufps.core_risk.controller.ResponsableController import *
from Risk_project_ufps.core_risk.controller.TareaController import *

from Risk_project_ufps.core_risk.dto.models import Proyecto

from Risk_project_ufps.core_risk.util.reporteEXCEL import *

from datetime import datetime
from operator import itemgetter, attrgetter

from django.forms.models import model_to_dict


class ReporteController:

    def generar_reporte_identificar(self, proyecto):
        """Llamar la función Exportar, la cuál esta en la clase reporteEXCEL,
       a esta clase le pasamos el título de la tabla, la cabecera, los
       registros y el nombre del archivo xlsx (EXCEL)."""
        propietario = proyecto.gerente.gerente_nombre
        titulo = "REPORTE PROYECTO " + proyecto.proyecto_nombre
        cabecera = ("CODIGO", "RIESGO", "CAUSAS", "EVENTO", "EFECTOS", "RESPONSABLE")
        riesgo_dao = RiesgoDao()
        riesgos = riesgo_dao.get_riesgos_by_proyecto(proyecto)
        registros = self.raw_queryset_as_values_list(riesgos)
        """registros = [(1110800310, "Andres", "Niño", "06/06/2019", "we", 43),
             (1110800311, "Andres", "Niño", "06/06/2019",  "we", 43),
             (1110800312, "Andres", "Niño", "06/06/2019",  "we", 43),
             ]"""
        nombreEXCEL = "reporte_" + self.get_datetime()
        reporte = reporteEXCEL(titulo, cabecera, registros, nombreEXCEL, propietario).Exportar()
        return nombreEXCEL + ".xlsx"

    def generar_reporte_planificar(self, proyecto):
        """Llamar la función Exportar, la cuál esta en la clase reporteEXCEL,
       a esta clase le pasamos el título de la tabla, la cabecera, los
       registros y el nombre del archivo xlsx (EXCEL)."""
        propietario = proyecto.gerente.gerente_nombre
        titulo = "REPORTE PROYECTO " + proyecto.proyecto_nombre
        cabecera = ("RESPONSABLE", "DESCRIPCION", "ROL")
        responsable_dao = ResponsableDao()
        responsables = responsable_dao.listar_responsables(proyecto.proyecto_id)
        registros = self.tamizar_responsables(responsables)
        nombreEXCEL = "reporte_" + self.get_datetime()
        reporte = reporteEXCEL(titulo, cabecera, registros, nombreEXCEL, propietario).Exportar_planificar(
            proyecto.proyecto_objetivo, proyecto.proyecto_alcance)
        return nombreEXCEL + ".xlsx"

    def generar_reporte_evaluar(self, proyecto: Proyecto):
        """Llamar la función Exportar, la cuál esta en la clase reporteEXCEL,
       a esta clase le pasamos el título de la tabla, la cabecera, los
       registros y el nombre del archivo xlsx (EXCEL)."""
        propietario = proyecto.gerente.gerente_nombre
        titulo = "REPORTE PROYECTO " + proyecto.proyecto_nombre
        cabecera = ("CÓDIGO", "RIESGO", "IMPACTO", "PROBABILIDAD", "TOTAL")
 
        riesgo_dao = RiesgoDao()
        clasificacion_dao = ClasificacionRiesgoDao()

        riesgos = riesgo_dao.get_riesgos_by_proyecto(proyecto)
        clasificaciones = clasificacion_dao.listar_clasificaciones_by_proyecto(proyecto) 

        registros = self.raw_queryset_as_values_list_evaluar(riesgos, proyecto)
        aux = sorted(registros, key=itemgetter(4), reverse=True)
        nombreEXCEL = "reporte_" + self.get_datetime()
        reporte = reporteEXCEL(titulo, cabecera, aux, nombreEXCEL, propietario).exportar_evaluar(
            proyecto.proyecto_objetivo, proyecto.proyecto_alcance, clasificaciones)
        return nombreEXCEL + ".xlsx"

    def generar_reporte_planificar_respuesta(self, proyecto):
        """
        :type proyecto: Proyecto
        """
        propietario = proyecto.gerente.gerente_nombre
        titulo = "REPORTE PROYECTO " + proyecto.proyecto_nombre
        cabecera = ("CÓDIGO", "RIESGO", "ACCIONES","TIPO DE ACCIÓN", "TAREAS", "RECURSOS")

        riesgo_controller = RiesgoController()
        respuesta_controller = RespuestaController()
        tarea_controller = TareaController()

        riesgos = riesgo_controller.get_riesgos_by_proyecto_aux(proyecto)
        respuestas_riesgo = respuesta_controller.listar_riesgos_respuesta(proyecto.proyecto_id)
        lista_tareas = tarea_controller.listar_tareas_group_by_riesgo(proyecto)

        mezcla = self.mezclar_respuestas_with_tareas(riesgos, respuestas_riesgo, lista_tareas)

        registros = self.convertir_array_2(mezcla)

        nombre_excel = "reporte_" + self.get_datetime()
        reporte = reporteEXCEL(titulo, cabecera, registros, nombre_excel, propietario)
        reporte.exportar_planificar_respuesta(proyecto.proyecto_objetivo, proyecto.proyecto_alcance)
        return nombre_excel + ".xlsx"

    def generar_reporte_controlar_riesgos(self, proyecto):
        """
                :type proyecto: Proyecto
                """
        propietario = proyecto.gerente.gerente_nombre
        titulo = "REPORTE PROYECTO " + proyecto.proyecto_nombre
        cabecera = ("ID", "TAREA", "FECHA INICIO PLANEADA", "FECHA FIN PLANEADA","DURACIÓN PLANEADA","FECHA INICIO REAL", "FECHA FIN REAL", "DURACION REAL", "% AVANCE ESPERADO", "% ATRASO", "ESTADO", "OBSERVACIONES")

        riesgo_controller = RiesgoController()
        respuesta_controller = RespuestaController()
        tarea_controller = TareaController()

        riesgos = riesgo_controller.get_riesgos_by_proyecto_linea(proyecto, proyecto.proyecto_linea_base)
        respuestas_riesgo = respuesta_controller.listar_riesgos_respuesta_base(proyecto.proyecto_id)
        lista_tareas = tarea_controller.listar_tareas_group_by_riesgo_base(proyecto)

        mezcla = self.mezclar_respuestas_with_tareas(riesgos, respuestas_riesgo, lista_tareas)

        #print('mezcla', mezcla)
        registros = self.convertir_array(mezcla)
        nombre_excel = "reporte_" + self.get_datetime()
        reporte = reporteEXCEL(titulo, cabecera, registros, nombre_excel, propietario)
        reporte.exportar_controlar_riesgos(proyecto.proyecto_objetivo, proyecto.proyecto_alcance)
        return nombre_excel + ".xlsx"

    def filtrar_respuestas_riesgo(self, respuestas, riesgo_id):
        key = "riesgo_"+str(riesgo_id)
        aux = respuestas.get(key)
        mensaje = ""
        if aux:
            for respuesta in aux:
                mensaje += mensaje + "- " + respuesta['respuesta_nombre'] + "\n"
        return mensaje

    def get_datetime(self):
        now = datetime.now()
        date_time = now.strftime("%m_%d_%Y")
        # print("date and time:",date_time)
        return date_time

    def raw_queryset_as_values_list(self, raw_qs):
        aux = []
        responsable_dao = ResponsableDao()
        for row in raw_qs:
            print("ROW", row)
            riesgo = model_to_dict(row)
            aux.append([
                "R_" + str(riesgo['riesgo_id']),
                riesgo['riesgo_nombre'],
                riesgo['riesgo_causa'],
                riesgo['riesgo_evento'],
                riesgo['riesgo_efecto'],
                responsable_dao.obtener_responsable(row.responsable_id).responsble_nombre                 
            ])
        return aux

    def raw_queryset_as_values_list_evaluar(self, raw_qs, proyecto):
        """

        :type proyecto: Proyecto
        """
        impacto_dao = ImpactoDao()
        probabilidad_dao = ProbabilidadDao()
        valores = {}
        aux = []
        for row in raw_qs:

            riesgo = model_to_dict(row)
            impacto = valores.get("i_" + str(row.riesgo_id))
            probabilidad = valores.get("p_" + str(row.riesgo_id))
            if impacto is None:
                impacto = impacto_dao.obtener_impacto_by_id_and_proyecto(row.impacto_id, proyecto)
                valores["i_" + str(row.riesgo_id)] = impacto
            if probabilidad is None:
                probabilidad = probabilidad_dao.obtener_probabilidad_by_id(row.propabilidad_id)
                valores["p_" + str(row.riesgo_id)] = probabilidad
            aux.append([
                "R_" + str(riesgo['riesgo_id']),
                riesgo['riesgo_nombre'],
                impacto.impacto_categoria,
                probabilidad.propabilidad_categoria,
                (impacto.impacto_valor * probabilidad.propabilidad_valor)
            ])
        return aux

    def tamizar_responsables(self, raw_qs):
        aux = []
        for row in raw_qs:
            responsable = model_to_dict(row)
            aux.append([
                responsable['responsble_nombre'],
                responsable['responsble_descripcion'],
                row.rol.rol_nombre
            ])
        return aux

    def mezclar_respuestas_with_tareas(self, riesgos, respuestas_riesgo, lista_tareas):
        riesgo_aux = {}
        for riesgo in riesgos:
            llave = 'riesgo_' + str(riesgo.riesgo_id)
            respuestas = respuestas_riesgo.get(llave)
            if respuestas:
                riesgo_aux[llave] = dict(
                    riesgo_id=riesgo.riesgo_id,
                    riesgo_nombre=riesgo.riesgo_nombre
                )
                for respuesta in respuestas:
                    riesgo_has_respuesta = respuesta['riesgo_has_respuesta']
                    tareas = lista_tareas[llave]
                    for tarea in tareas:                        
                        if tarea['riesgo_has_respuesta'] == riesgo_has_respuesta:
                            if respuesta.get('tareas'):
                                respuesta['tareas'].append(tarea)
                            else:
                                respuesta['tareas'] = []
                                respuesta['tareas'].append(tarea)
                    if riesgo_aux[llave].get('respuestas'):
                        riesgo_aux[llave]['respuestas'].append(respuesta)
                    else:
                        riesgo_aux[llave]['respuestas'] = []
                        riesgo_aux[llave]['respuestas'].append(respuesta)
        return riesgo_aux

    def convertir_array(self, mezcla):
        array_final = []
        contador = 1;
        for key, aux in mezcla.items():
            respuestas = aux.get('respuestas')
            if respuestas and len(respuestas) > 0:
                for aux_2 in respuestas:
                    #print("ARRAY", aux_2)
                    tareas = aux_2.get('tareas')
                    if tareas and len(tareas) > 0:
                        for aux_3 in tareas:
                            array_final.append([ 
                                contador,                               
                                aux_3['tarea_nombre'],
                                aux_3['fecha_inicio'],
                                aux_3['fecha_fin'],
                                aux_3['duracion'],
                                self.split_fecha(aux_3['fecha_inicio_real']) ,
                                self.split_fecha(aux_3['fecha_fin_real']),
                                aux_3['duracion_real'],
                                str(self.calcular_porcentaje_avance(int(aux_3["tarea_estado"]), aux_3['fecha_inicio'], aux_3['fecha_fin'], int(aux_3["duracion"]))) + '%',
                                str(self.calcular_porcentaje_atraso(int(aux_3['duracion']), int(aux_3['duracion_real'])))+ '%',
                                self.get_estado(aux_3['tarea_estado']),
                                aux_3['tarea_observacion'],
                            ])
                    else:
                        array_final.append([
                            aux['riesgo_nombre'],
                            aux_2['respuesta_nombre'],
                            aux_2['tipo_respuesta'],
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                        ])
                contador = contador+1
            else:
                array_final.append([
                    aux['riesgo_nombre'],
                    'riesgo no posee acciones',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                ])
        return array_final

    def convertir_array_2(self, mezcla):
        array_final = []
        for key, aux in mezcla.items():
            respuestas = aux.get('respuestas')
            if respuestas and len(respuestas) > 0:
                for aux_2 in respuestas:
                    # print("ARRAY", aux_2)
                    tareas = aux_2.get('tareas')
                    if tareas and len(tareas) > 0:
                        for aux_3 in tareas:
                            array_final.append([
                                "R"+str(aux['riesgo_id']),
                                aux['riesgo_nombre'],
                                aux_2['respuesta_nombre'],
                                aux_2['tipo_respuesta'],
                                aux_3['tarea_nombre'],                            
                                self.parsear_recursos(aux_3['recursos'])
                            ])
                    else:
                        array_final.append([
                            "R" + str(aux['riesgo_id']),
                            aux['riesgo_nombre'],
                            aux_2['respuesta_nombre'],
                            aux_2['tipo_respuesta'],
                            'No hay tareas',
                        ])
            else:
                array_final.append([
                    "R" + str(aux['riesgo_id']),
                    aux['riesgo_nombre'],
                    'riesgo no posee acciones',
                ])
        return array_final

    def get_estado(self, valor):
        if valor == 1:
            return 'No iniciado'
        elif valor == 2:
            return 'Iniciado'
        elif valor == 3:
            return 'Completado'
        else:
            return 'Retrasado'

    def calcular_porcentaje_atraso(self, duracion_planeada:int, duracion_real:int):
        dife = duracion_real-duracion_planeada
        porc = (dife * 100) / duracion_planeada
        if porc < 0:
            porc = 0.0
        return porc

    def calcular_porcentaje_avance(self, estado:int, fecha_inicio_planeada:str, fecha_fin_planeada:str, duracion_planeada:int):
        fecha_inicio = datetime.strptime(fecha_inicio_planeada, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_planeada, '%Y-%m-%d')
        if estado == 1:
            return 0.0
        elif estado == 3:
            return 100
        fecha_actual = datetime.now()
        dife = (fecha_actual - fecha_inicio).days
        return round((dife*100)/duracion_planeada,2)


    def split_fecha(self, fecha):

        var = fecha.split("T")
        return var[0]

    def parsear_recursos(self, recursos):
        aux = ""
        for recurso in recursos:            
            aux += "- "+recurso['recurso_nombre']
            aux += " -- costo: $"+str(recurso['recurso_costo'])
            aux += " -- cant: "+str(recurso['cantidad'])
            aux += " -- total: "+str(int((recurso['cantidad']))*int((recurso['recurso_costo'])) )+"\n"
        return aux
