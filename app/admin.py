from django.contrib import admin
from .models import Landing, Lead, Post


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("creado", "landing", "nombre", "empresa", "correo", "celular", "estado")
    list_filter = ("landing", "estado", "creado")
    search_fields = ("nombre", "empresa", "correo", "celular")
    list_editable = ("estado",)
    readonly_fields = ("creado",)


@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "ruta", "activa")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "landing", "publicado", "fecha_publicacion", "autor")
    list_filter = ("landing", "publicado")
    search_fields = ("titulo", "resumen")
    readonly_fields = ("slug", "creado", "actualizado")