from Risk_project_ufps.core_risk.dto.models import Pais

class PaisDao:

  def listar_paises(self):
    paises = {}
    try:
      paises = Pais.objects.all()
    except Exception as e:
      print(e)
    return paises