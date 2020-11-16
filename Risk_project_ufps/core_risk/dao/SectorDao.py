from Risk_project_ufps.core_risk.dto.models import Sector


class SectorDao:

    def listar_sectores(self):
        sectores = {}
        try:
            sectores = Sector.objects.all().order_by('sector_nombre')
        except Exception as e:
            print(e)
        return sectores

    def obtener_sector(self, id):
        sector = {}
        try:
            sector = Sector.objects.get(sector_id=id)
        except Exception as e:
            print(e)
        return sector
