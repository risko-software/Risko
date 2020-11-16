from Risk_project_ufps.core_risk.dao import ComentarioDao


def crear_comentario(fecha, nombre, correo, mensaje):
    return ComentarioDao.crear_comentario(fecha, nombre, correo, mensaje)
