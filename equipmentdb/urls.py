from django.urls import path
from django.views.generic import TemplateView
import equipmentdb.views as views
import inspect
from equipmentdb.model_base import classToURL
from equipmentdb.views import (
    UbucBaseListView,
    UbucBaseCreateView,
    UbucBaseUpdateView,
    UbucBaseUpdateView,
)

def generatePath(view_class):
    
        model_url = classToURL(view_class.model.__name__)
        if UbucBaseListView in view_class.__bases__:
            return path(model_url, view_class.as_view(), name=f"{model_url}-list")
        if UbucBaseCreateView in view_class.__bases__:
            return path(
                f"{model_url}/add", view_class.as_view(), name=f"{model_url}-add"
            )
        if UbucBaseUpdateView in view_class.__bases__:
            return path(
                f"{model_url}/<int:pk>",
                view_class.as_view(),
                name=f"{model_url}-update",
            )
        if UbucBaseUpdateView in view_class.__bases__:
            return path(
                f"{model_url}/<int:pk>/delete",
                view_class.as_view(),
                name=f"{model_url}-delete",
            )


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", TemplateView.as_view(template_name="about.html")),
]

urlpatterns += [
    generatePath(view_class)
    for n, view_class in inspect.getmembers(views, inspect.isclass)
    if "model" in view_class.__dict__
    and view_class.__bases__[0]
    in [
        UbucBaseListView,
        UbucBaseCreateView,
        UbucBaseUpdateView,
        UbucBaseUpdateView,
    ]
]
# path(
#     "equipment-types", EquipmentTypeListView.as_view(), name="equipment-type-list"
# ),
# path(
#     "equipment-types/add",
#     EquipmentTypeCreateView.as_view(),
#     name="equipment-type-add",
# ),
# path(
#     "equipment-types/<int:pk>",
#     EquipmentTypeUpdateView.as_view(),
#     name="equipment-type-update",
# ),
# path(
#     "equipment-types/<int:pk>/delete",
#     EquipmentTypeDeleteView.as_view(),
#     name="equipment-type-delete",
# ),
# path("equipment", EquipmentListView.as_view(), name="equipment-list"),
# path(
#     "equipment/add",
#     EquipmentCreateView.as_view(),
#     name="equipment-add",
# ),
# path(
#     "equipment/<int:pk>",
#     EquipmentUpdateView.as_view(),
#     name="equipment-update",
# ),
# path(
#     "equipment/<int:pk>/delete",
#     EquipmentDeleteView.as_view(),
#     name="equipmentdelete",
# ),
# path("equipment-note", EquipmentNoteListView.as_view(), name="equipment-note-list"),
# path(
#     "equipment-note/add",
#     EquipmentNoteCreateView.as_view(),
#     name="equipment-note-add",
# ),
# path(
#     "equipment-note/<int:pk>",
#     EquipmentNoteUpdateView.as_view(),
#     name="equipment-note-update",
# ),
# path(
#     "equipment-note/<int:pk>/delete",
#     EquipmentNoteDeleteView.as_view(),
#     name="equipment-notedelete",
# ),
# path(
#     "equipment-type-service-schedule",
#     EquipmentTypeServiceScheduleListView.as_view(),
#     name="equipment-type-service-schedule-list",
# ),
# path(
#     "equipment-type-service-schedule/add",
#     EquipmentTypeServiceScheduleCreateView.as_view(),
#     name="equipment-type-service-schedule-add",
# ),
# path(
#     "equipment-type-service-schedule/<int:pk>",
#     EquipmentTypeServiceScheduleUpdateView.as_view(),
#     name="equipment-type-service-schedule-update",
# ),
# path(
#     "equipment-type-service-schedule/<int:pk>/delete",
#     EquipmentTypeServiceScheduleDeleteView.as_view(),
#     name="equipment-type-service-scheduledelete",
# ),
# path(
#     "equipment-type-test-schedule",
#     EquipmentTypeTestScheduleListView.as_view(),
#     name="equipment-type-test-schedule-list",
# ),
# path(
#     "equipment-type-test-schedule/add",
#     EquipmentTypeTestScheduleCreateView.as_view(),
#     name="equipment-type-test-schedule-add",
# ),
# path(
#     "equipment-type-test-schedule/<int:pk>",
#     EquipmentTypeTestScheduleUpdateView.as_view(),
#     name="equipment-type-test-schedule-update",
# ),
# path(
#     "equipment-type-test-schedule/<int:pk>/delete",
#     EquipmentTypeTestScheduleDeleteView.as_view(),
#     name="equipment-type-test-scheduledelete",
# ),
# path(
#     "test-type",
#     TestTypeListView.as_view(),
#     name="test-type-list",
# ),
# path(
#     "test-type/add",
#     TestTypeCreateView.as_view(),
#     name="test-type-add",
# ),
# path(
#     "test-type/<int:pk>",
#     TestTypeUpdateView.as_view(),
#     name="test-type-update",
# ),
# path(
#     "test-type/<int:pk>/delete",
#     TestTypeDeleteView.as_view(),
#     name="test-typedelete",
# ),
# ]
