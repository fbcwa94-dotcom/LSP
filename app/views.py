import csv

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LeadForm, PostForm
from .models import Lead, Post

# Solo usuarios con sesión iniciada y marcados como "staff"
solo_staff = user_passes_test(lambda u: u.is_active and u.is_staff)




def landing(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.utm_source = request.GET.get("utm_source", "")[:100]
            lead.utm_medium = request.GET.get("utm_medium", "")[:100]
            lead.utm_campaign = request.GET.get("utm_campaign", "")[:100]
            lead.save()
            messages.success(request, "¡Gracias! Un productor te contactará en menos de 12 horas.")
            return redirect("landing")
    else:
        form = LeadForm()
    return render(request, "SLProducciones.html", {"form": form})





def _leads_filtrados(request):
    leads = Lead.objects.all()
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "")

    if q:
        leads = leads.filter(
            Q(nombre__icontains=q) | Q(empresa__icontains=q)
            | Q(correo__icontains=q) | Q(celular__icontains=q)
        )
    if estado:
        leads = leads.filter(estado=estado)
    return leads, q, estado


@solo_staff
def panel(request):
    leads, q, estado = _leads_filtrados(request)
    pagina = Paginator(leads, 50).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "panel_leads.html", {
        "pagina": pagina,
        "total": pagina.paginator.count,
        "q": q,
        "estado": estado,
        "estados": Lead.Estado.choices,
        "qs": params.urlencode(),
    })


def _celda_segura(valor):
    texto = "" if valor is None else str(valor)
    return "'" + texto if texto[:1] in ("=", "+", "-", "@") else texto


@solo_staff
def panel_csv(request):
    leads, _, _ = _leads_filtrados(request)
    fecha = timezone.localdate().strftime("%Y-%m-%d")
    respuesta = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    respuesta["Content-Disposition"] = f'attachment; filename="leads_{fecha}.csv"'

    escritor = csv.writer(respuesta, delimiter=";")
    escritor.writerow(["Fecha", "Nombre", "Cargo", "Empresa", "Correo", "Celular",
                       "Mensaje", "Estado", "UTM source", "UTM medium", "UTM campaign"])
    for lead in leads:
        escritor.writerow([_celda_segura(v) for v in (
            timezone.localtime(lead.creado).strftime("%d/%m/%Y %H:%M"),
            lead.nombre, lead.cargo, lead.empresa, lead.correo, lead.celular,
            lead.mensaje, lead.get_estado_display(),
            lead.utm_source, lead.utm_medium, lead.utm_campaign,
        )])
    return respuesta

def blog_lista(request):
    posts = Post.objects.filter(publicado=True)
    pagina = Paginator(posts, 9).get_page(request.GET.get("page"))
    return render(request, "blog_lista.html", {"pagina": pagina})


def blog_detalle(request, slug):
    qs = Post.objects.select_related("autor")
    if not request.user.is_staff:
        qs = qs.filter(publicado=True)
    return render(request, "blog_detalle.html", {"post": get_object_or_404(qs, slug=slug)})




@solo_staff
def panel_blog(request):
    return render(request, "panel_blog_lista.html", {"posts": Post.objects.select_related("autor")})


@solo_staff
def panel_blog_form(request, pk=None):
    post = get_object_or_404(Post, pk=pk) if pk else None
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == "POST" and form.is_valid():
        nuevo = form.save(commit=False)
        if nuevo.autor_id is None:
            nuevo.autor = request.user
        nuevo.save()
        messages.success(request, "Artículo guardado.")
        return redirect("panel_blog")

    return render(request, "panel_blog_form.html", {"form": form, "post": post})


@solo_staff
@require_POST
def panel_blog_eliminar(request, pk):
    get_object_or_404(Post, pk=pk).delete()
    messages.success(request, "Artículo eliminado.")
    return redirect("panel_blog")