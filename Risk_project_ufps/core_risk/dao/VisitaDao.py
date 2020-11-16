from Risk_project_ufps.core_risk.dto.models import Visitas


def crear_visita(fecha_visita):
    visita = None
    try:
        visita = Visitas(fecha_visita=fecha_visita)
        visita.save()
    except Exception as e:
        print(e)
    return visita


def get_cantidad_visitas():
    return Visitas.objects.count()
