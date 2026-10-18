from django.urls import path
from . import views

urlpatterns = [
    path("SLProduction/", views.SLP, name="SLProduction"),
    path("carreta/", views.carreta, name="carreta"),
    path("geletao/", views.geletao, name="geletao"),
    # Blog público
    path("blog/<slug:landing_slug>/", views.blog_lista, name="blog_lista"),
    path("blog/<slug:landing_slug>/<slug:slug>/", views.blog_detalle, name="blog_detalle"),

# Panel del blog (antes de panel/<slug:slug>/)
    path("panel/blog/", views.panel_blog, name="panel_blog"),
    path("panel/blog/nuevo/", views.panel_blog_form, name="panel_blog_nuevo"),
    path("panel/blog/<int:pk>/editar/", views.panel_blog_form, name="panel_blog_editar"),
    path("panel/blog/<int:pk>/eliminar/", views.panel_blog_eliminar, name="panel_blog_eliminar"),
    path("panel/", views.panel, name="panel"),
    path("panel/<slug:slug>/csv/", views.panel_csv, name="panel_csv"),
    path("panel/<slug:slug>/", views.panel, name="panel_landing"),
    

# ...luego tus rutas de login, panel y panel/<slug:slug>/

]