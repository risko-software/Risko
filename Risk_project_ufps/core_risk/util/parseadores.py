def tarea_to_dict(tarea):
    return dict(
        tarea_id=tarea.tarea_id,
        tarea_nombre=tarea.tarea_nombre,
        tarea_descripcion=tarea.tarea_descripcion,
        proyecto_has_riesgo=tarea.proyecto_has_riesgo,
        riesgo_has_respuesta=tarea.riesgo_has_respuesta,
        fecha_inicio=tarea.fecha_inicio,
        duracion=tarea.duracion,
        fecha_fin=tarea.fecha_fin,
        fecha_inicio_real=tarea.fecha_inicio_real,
        duracion_real=tarea.duracion_real,
        fecha_fin_real=tarea.fecha_fin_real,
        tarea_observacion=tarea.tarea_observacion,
        tarea_estado=tarea.tarea_estado,
        proyecto_linea_base=tarea.proyecto_linea_base
    )