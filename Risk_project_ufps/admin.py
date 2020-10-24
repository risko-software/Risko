from django.contrib import admin

from Risk_project_ufps.core_risk.dto.models import Gerente
from Risk_project_ufps.core_risk.dto.models import Comentario
from Risk_project_ufps.core_risk.dto.models import Visitas
from Risk_project_ufps.core_risk.dto.models import Sector

admin.site.register(Gerente)
admin.site.register(Comentario)
admin.site.register(Visitas)
admin.site.register(Sector)

