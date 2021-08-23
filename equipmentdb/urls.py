from django.urls import path
from django.views.generic import TemplateView
from equipmentdb.views import (
    EquipmentTypeDeleteView,
    EquipmentTypeListView,
    EquipmentTypeCreateView,
    EquipmentTypeUpdateView,
)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", TemplateView.as_view(template_name="about.html")),
    path(
        "equipment-types", EquipmentTypeListView.as_view(), name="equipment-type-list"
    ),
    path(
        "equipment-types/add",
        EquipmentTypeCreateView.as_view(),
        name="equipment-type-add",
    ),
    path(
        "equipment-types/<int:pk>",
        EquipmentTypeUpdateView.as_view(),
        name="equipment-type-update",
    ),
    path(
        "equipment-types/<int:pk>/delete",
        EquipmentTypeDeleteView.as_view(),
        name="equipment-type-delete",
    ),
]
