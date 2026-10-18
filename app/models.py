from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import re
import nh3
from django.template.defaultfilters import linebreaks_filter
from django.utils.safestring import mark_safe


from django.urls import NoReverseMatch, reverse

TAGS_PERMITIDOS = {"p", "br", "h2", "h3", "strong", "em", "u", "s", "ul", "ol", "li", "blockquote", "a"}
ATRIBUTOS_PERMITIDOS = {
    "a": {"href", "target"},
    "p": {"class"}, "h2": {"class"}, "h3": {"class"}, "blockquote": {"class"},
}
ES_HTML = re.compile(r"<(p|h2|h3|ul|ol|blockquote)\b", re.IGNORECASE)

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    resumen = models.CharField(max_length=300)
    portada = models.ImageField(upload_to="blog/", blank=True)
    contenido = models.TextField()
    publicado = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="posts",
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-fecha_publicacion", "-creado"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("blog_detalle", args=[self.slug]) if self.slug else ""

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200] or "articulo"
            slug, n = base, 2
            while Post.objects.filter(slug=slug).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        if self.publicado and not self.fecha_publicacion:
            self.fecha_publicacion = timezone.now()
        if ES_HTML.search(self.contenido):
            self.contenido = nh3.clean(
                self.contenido,
                tags=TAGS_PERMITIDOS,
                attributes=ATRIBUTOS_PERMITIDOS,
                url_schemes={"http", "https", "mailto"},
                link_rel="noopener noreferrer",
            )
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("blog_detalle", args=[self.slug]) if self.slug else ""


    @property
    def contenido_html(self):
        """HTML ya limpio, o texto plano convertido a párrafos (artículos antiguos)."""
        if ES_HTML.search(self.contenido):
            return mark_safe(self.contenido)
        return linebreaks_filter(self.contenido)



class Lead(models.Model):
    class Estado(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        CONTACTADO = "contactado", "Contactado"
        COTIZADO = "cotizado", "Cotizado"
        CERRADO = "cerrado", "Cerrado"
        DESCARTADO = "descartado", "Descartado"

    nombre = models.CharField(max_length=120)
    cargo = models.CharField(max_length=120, blank=True)
    empresa = models.CharField(max_length=150)
    correo = models.EmailField("correo corporativo")
    celular = models.CharField("celular / WhatsApp", max_length=30)
    mensaje = models.TextField("¿Qué quieres que viva tu equipo?", blank=True)

    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NUEVO)
    creado = models.DateTimeField(auto_now_add=True)

    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.nombre} · {self.empresa}"
    class Estado(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        CONTACTADO = "contactado", "Contactado"
        COTIZADO = "cotizado", "Cotizado"
        CERRADO = "cerrado", "Cerrado"
        DESCARTADO = "descartado", "Descartado"

    # Datos del formulario
    nombre = models.CharField(max_length=120)
    cargo = models.CharField(max_length=120, blank=True)
    empresa = models.CharField(max_length=150)
    correo = models.EmailField("correo corporativo")
    celular = models.CharField("celular / WhatsApp", max_length=30)
    mensaje = models.TextField("¿Qué quieres que viva tu equipo?", blank=True)

    # Seguimiento
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.NUEVO
    )
    creado = models.DateTimeField(auto_now_add=True)

    # Origen de la campaña (opcional, vienen de la URL ?utm_source=...)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-creado"]
        indexes = [models.Index(fields=[ "-creado"])]

    def __str__(self):
        return f"{self.nombre} · {self.empresa} ({self.landing.slug})"