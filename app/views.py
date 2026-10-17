from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LeadForm
from .models import Landing, Lead
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
import csv
from django.utils import timezone


from .models import Landing


def landing_view(request: HttpRequest, slug: str, template: str) -> HttpResponse:
    landing = get_object_or_404(Landing, slug=slug, activa=True)

    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.landing = landing
            lead.utm_source = request.GET.get("utm_source", "")[:100]
            lead.utm_medium = request.GET.get("utm_medium", "")[:100]
            lead.utm_campaign = request.GET.get("utm_campaign", "")[:100]
            lead.save()
            messages.success(request, "¡Gracias! Un productor te contactará en menos de 12 horas.")
            return redirect(request.path)  # evita reenvío al recargar
    else:
        form = LeadForm()

    return render(request, template, {"form": form, "landing": landing})


# Una función por landing, reutilizando la lógica
def SLP(request):
    return landing_view(request, slug="sl-producciones", template="SLProducciones.html")

def carreta(request):
    return landing_view(request, slug="carreta", template="landing_carreta.html")

def geletao(request):
    return landing_view(request, slug="geletao", template="landing_geletao.html")

@staff_member_required
def panel(request, slug=None):
    landings = Landing.objects.annotate(total=Count("leads")).order_by("nombre")

    # Sin slug en la URL: abre la primera landing
    if slug is None:
        primera = landings.first()
        if primera:
            return redirect("panel_landing", slug=primera.slug)
        return render(request, "panel_leads.html", {"landings": landings})

    seleccionada = get_object_or_404(Landing, slug=slug)
    leads = seleccionada.leads.all()

    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "")

    if q:
        leads = leads.filter(
            Q(nombre__icontains=q)
            | Q(empresa__icontains=q)
            | Q(correo__icontains=q)
            | Q(celular__icontains=q)
        )
    if estado:
        leads = leads.filter(estado=estado)

    return render(request, "panel_leads.html", {
        "landings": landings,
        "seleccionada": seleccionada,
        "leads": leads,
        "q": q,
        "estado": estado,
        "estados": Lead.Estado.choices,
    })

def _leads_filtrados(request, landing):
    """Aplica buscador y estado. Lo usan el panel y la descarga CSV."""
    leads = landing.leads.all()
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "")

    if q:
        leads = leads.filter(
            Q(nombre__icontains=q)
            | Q(empresa__icontains=q)
            | Q(correo__icontains=q)
            | Q(celular__icontains=q)
        )
    if estado:
        leads = leads.filter(estado=estado)
    return leads, q, estado


@staff_member_required
def panel(request, slug=None):
    landings = Landing.objects.annotate(total=Count("leads")).order_by("nombre")

    if slug is None:
        primera = landings.first()
        if primera:
            return redirect("panel_landing", slug=primera.slug)
        return render(request, "panel_leads.html", {"landings": landings})

    seleccionada = get_object_or_404(Landing, slug=slug)
    leads, q, estado = _leads_filtrados(request, seleccionada)

    return render(request, "panel_leads.html", {
        "landings": landings,
        "seleccionada": seleccionada,
        "leads": leads,
        "q": q,
        "estado": estado,
        "estados": Lead.Estado.choices,
    })


def _celda_segura(valor):
    """Evita que Excel ejecute fórmulas si un texto empieza con = + - @."""
    texto = "" if valor is None else str(valor)
    return "'" + texto if texto[:1] in ("=", "+", "-", "@") else texto


@staff_member_required
def panel_csv(request, slug):
    landing = get_object_or_404(Landing, slug=slug)
    leads, _, _ = _leads_filtrados(request, landing)

    fecha = timezone.localdate().strftime("%Y-%m-%d")
    respuesta = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    respuesta["Content-Disposition"] = f'attachment; filename="leads_{landing.slug}_{fecha}.csv"'

    escritor = csv.writer(respuesta, delimiter=";")
    escritor.writerow([
        "Fecha", "Nombre", "Cargo", "Empresa", "Correo", "Celular",
        "Mensaje", "Estado", "UTM source", "UTM medium", "UTM campaign",
    ])
    for lead in leads:
        escritor.writerow([_celda_segura(v) for v in (
            timezone.localtime(lead.creado).strftime("%d/%m/%Y %H:%M"),
            lead.nombre, lead.cargo, lead.empresa, lead.correo, lead.celular,
            lead.mensaje, lead.get_estado_display(),
            lead.utm_source, lead.utm_medium, lead.utm_campaign,
        )])
    return respuesta