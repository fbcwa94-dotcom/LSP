from django.contrib import admin
from .models import Landing, Lead


@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "activa")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("creado", "landing", "nombre", "empresa", "correo", "celular", "estado")
    list_filter = ("landing", "estado", "creado")
    search_fields = ("nombre", "empresa", "correo", "celular")
    list_editable = ("estado",)
    readonly_fields = ("creado",)