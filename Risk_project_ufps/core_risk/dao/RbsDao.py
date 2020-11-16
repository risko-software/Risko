from Risk_project_ufps.core_risk.dto.models import Rbs


class RbsDao:

    def get_rbs_gerente_id(self, gerente):
        rbs = None
        try:
            rbs = Rbs.objects.get(gerente=gerente)
        except Exception as inst:
            print(inst)
        return rbs

    def crear_rbs(self, gerente, rbs_default=None):
        rbs = None
        try:
            if rbs_default:
                rbs = Rbs(gerente=gerente, rbs_default=rbs_default)
            else:
                rbs = Rbs(gerente=gerente, rbs_default=0)
            rbs.save()
        except Exception as inst:
            print(inst)
        return rbs

    def crear_rbs_sugerida(self, gerente):
        rbs = None
        try:
            rbs = Rbs(gerente=gerente, rbs_default=1)
            rbs.save()
        except Exception as inst:
            print(inst)
        return rbs
