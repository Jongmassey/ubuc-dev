from django.urls import path
from django.views.generic import TemplateView

import inspect
from equipmentdb.model_base import classToURL
from equipmentdb.views import (
    UbucBaseListView,
    UbucBaseCreateView,
    UbucBaseUpdateView,
    UbucBaseUpdateView,
    index
)


def generatePath(view_class):

    model_url = classToURL(view_class.model.__name__)
    if UbucBaseListView in view_class.__bases__:
        return path(model_url, view_class.as_view(), name=f"{model_url}-list")
    if UbucBaseCreateView in view_class.__bases__:
        return path(f"{model_url}/add", view_class.as_view(), name=f"{model_url}-add")
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
    path("", index, name="index"),
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
