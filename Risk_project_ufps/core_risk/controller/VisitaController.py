from Risk_project_ufps.core_risk.dao import VisitaDao


def crear_visita(fecha_visita):
    return VisitaDao.crear_visita(fecha_visita)


def get_cantidad_visitas():
    return VisitaDao.get_cantidad_visitas()
