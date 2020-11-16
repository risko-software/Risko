from Risk_project_ufps.core_risk.dto.models import Comentario


def crear_comentario(fecha, nombre, correo, mensaje):
    comentario = None
    try:
        comentario = Comentario(comentario_fecha=fecha,
                                comentario_nombre=nombre,
                                comentario_correo=correo,
                                comentario_mensaje=mensaje)
        comentario.save()
    except Exception as e:
        print(e)
    return comentario
