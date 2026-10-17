from django.db import models


class Landing(models.Model):
    """Cada página de captura. Ej: slug='carreta', nombre='Fiestas Carreta'."""
    slug = models.SlugField("identificador", max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Lead(models.Model):
    class Estado(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        CONTACTADO = "contactado", "Contactado"
        COTIZADO = "cotizado", "Cotizado"
        CERRADO = "cerrado", "Cerrado"
        DESCARTADO = "descartado", "Descartado"

    # De qué página viene
    landing = models.ForeignKey(
        Landing, on_delete=models.PROTECT, related_name="leads"
    )

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
        indexes = [models.Index(fields=["landing", "-creado"])]

    def __str__(self):
        return f"{self.nombre} · {self.empresa} ({self.landing.slug})"