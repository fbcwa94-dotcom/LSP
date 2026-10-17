from django.urls import path
from . import views

urlpatterns = [
    path("SLP/", views.SLP, name="sl"),
    path("carreta/", views.carreta, name="carreta"),
    path("geletao/", views.geletao, name="geletao"),
    path("panel/", views.panel, name="panel"),
path("panel/<slug:slug>/csv/", views.panel_csv, name="panel_csv"),
path("panel/<slug:slug>/", views.panel, name="panel_landing"),

]