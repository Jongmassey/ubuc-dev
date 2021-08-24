from django.urls import path
from django.views.generic import TemplateView
from equipmentdb.views import *

urlpatterns = [
    path("", index, name="index"),
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
    path("equipment", EquipmentListView.as_view(), name="equipment-list"),
    path(
        "equipment/add",
        EquipmentCreateView.as_view(),
        name="equipment-add",
    ),
    path(
        "equipment/<int:pk>",
        EquipmentUpdateView.as_view(),
        name="equipment-update",
    ),
    path(
        "equipment/<int:pk>/delete",
        EquipmentDeleteView.as_view(),
        name="equipmentdelete",
    ),
]
