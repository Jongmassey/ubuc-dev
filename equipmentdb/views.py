from equipmentdb.models import EquipmentType
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from equipmentdb.models import *
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def index(request):
    return HttpResponse("Hello, world. You're at the equipmentdb index.")


class EquipmentTypeListView(ListView):
    model = EquipmentType
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class EquipmentTypeCreateView(CreateView):
    model = EquipmentType
    fields = ["name"]
    template_name_suffix = "_add_form"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EquipmentTypeCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        return super(EquipmentTypeCreateView, self).form_valid(form)


class EquipmentTypeUpdateView(UpdateView):
    model = EquipmentType
    fields = ["name"]
    template_name_suffix = "_update_form"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EquipmentTypeCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super(EquipmentTypeCreateView, self).form_valid(form)


class EquipmentTypeDeleteView(DeleteView):
    model = EquipmentType
    success_url = reverse_lazy("equipment-type-list")
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EquipmentTypeCreateView, self).dispatch(*args, **kwargs)
