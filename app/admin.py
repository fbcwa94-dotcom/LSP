from django.contrib import admin
from .models import Lead, Post


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("creado", "nombre", "empresa", "correo", "celular", "estado")
    list_filter = ("estado", "creado")
    search_fields = ("nombre", "empresa", "correo", "celular")
    list_editable = ("estado",)
    readonly_fields = ("creado",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "publicado", "fecha_publicacion", "autor")
    list_filter = ("publicado",)
    search_fields = ("titulo", "resumen")
    readonly_fields = ("slug", "creado", "actualizado")