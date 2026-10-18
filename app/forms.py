from django import forms
from .models import Lead, Post
from django.utils.html import strip_tags


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["nombre", "cargo", "empresa", "correo", "celular", "mensaje"]



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["landing", "titulo", "resumen", "portada", "contenido", "publicado"]

    def clean_portada(self):
        portada = self.cleaned_data.get("portada")
        if portada and hasattr(portada, "size") and portada.size > 3 * 1024 * 1024:
            raise forms.ValidationError("La imagen supera los 3 MB.")
        return portada
    
    def clean_contenido(self):
        contenido = self.cleaned_data["contenido"]
        texto = strip_tags(contenido).replace("&nbsp;", " ").strip()
        if not texto:
            raise forms.ValidationError("El contenido no puede estar vacío.")
        if len(contenido) > 100_000:
            raise forms.ValidationError("El artículo es demasiado largo (máximo 100.000 caracteres).")
        return contenido