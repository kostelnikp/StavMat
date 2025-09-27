from django.contrib import admin
from .models import Faktura, Projekt, Zakaznici, Praca, Zamestnanec, PouzityMaterial, Material

# Register your models here.

admin.site.register(Faktura)
admin.site.register(Projekt)
admin.site.register(Zakaznici)
admin.site.register(Praca)
admin.site.register(Zamestnanec)
admin.site.register(PouzityMaterial)
admin.site.register(Material)
