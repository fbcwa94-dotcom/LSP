from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),

    # Blog público
    path("blog/", views.blog_lista, name="blog_lista"),
    path("blog/<slug:slug>/", views.blog_detalle, name="blog_detalle"),

    # Acceso
    path("panel/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("panel/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Panel
    path("panel/", views.panel, name="panel"),
    path("panel/csv/", views.panel_csv, name="panel_csv"),
    path("panel/blog/", views.panel_blog, name="panel_blog"),
    path("panel/blog/nuevo/", views.panel_blog_form, name="panel_blog_nuevo"),
    path("panel/blog/<int:pk>/editar/", views.panel_blog_form, name="panel_blog_editar"),
    path("panel/blog/<int:pk>/eliminar/", views.panel_blog_eliminar, name="panel_blog_eliminar"),
]