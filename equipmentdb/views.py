from django.db.models.fields import DateField
from equipmentdb.models import EquipmentType
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from equipmentdb.models import *
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from django.forms import inlineformset_factory
from django.template import loader

class DateInput(forms.DateInput):
    input_type = "date"

def index(request):
    template = loader.get_template('equipmentdb/index.html')
    return HttpResponse(template.render())

#base views
class UbucBaseListView(ListView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class UbucBaseCreateView(CreateView):
    fields = "__all__"
    template_name_suffix = "_add_form"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UbucBaseCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        return super(UbucBaseCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        for f in self.model._meta.get_fields(
            include_parents=False, include_hidden=False
        ):
            if isinstance(f, DateField) and f.name in form.fields:
                form.fields[f.name].widget = DateInput()
        return form

class UbucBaseUpdateView(UpdateView):
    model = EquipmentType
    fields = "__all__"
    template_name_suffix = "_update_form"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UbucBaseUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.updated_by = self.request.user
        return super(UbucBaseUpdateView, self).form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        for f in self.model._meta.get_fields(
            include_parents=False, include_hidden=False
        ):
            if isinstance(f, DateField) and f.name in form.fields:
                form.fields[f.name].widget = DateInput()
        return form

class UbucBaseDeleteView(DeleteView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UbucBaseDeleteView, self).dispatch(*args, **kwargs)

# equipment types
class EquipmentTypeListView(UbucBaseListView):
    model = EquipmentType

class EquipmentTypeCreateView(UbucBaseCreateView):
    model = EquipmentType

class EquipmentTypeUpdateView(UbucBaseUpdateView):
    model = EquipmentType

class EquipmentTypeDeleteView(UbucBaseDeleteView):
    model = EquipmentType
    success_url = reverse_lazy("equipment-type-list")

# equipment items
class EquipmentListView(UbucBaseListView):
    model = Equipment

class EquipmentCreateView(UbucBaseCreateView):
    model = Equipment

class EquipmentUpdateView(UbucBaseUpdateView):
    model = Equipment
    NoteFormSet = inlineformset_factory(Equipment,EquipmentNote,fields=('notes',),extra=1)   

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        eqp = self.get_object()
        notes = self.NoteFormSet(instance=eqp)
        ctx['notes'] = notes
        return ctx

class EquipmentDeleteView(UbucBaseDeleteView):
    model = Equipment
    success_url = reverse_lazy("equipment-list")

# Equipment Notes
class EquipmentNoteListView(UbucBaseListView):
    model = EquipmentNote

class EquipmentNoteCreateView(UbucBaseCreateView):
    model = EquipmentNote

class EquipmentNoteUpdateView(UbucBaseUpdateView):
    model = EquipmentNote

class EquipmentNoteDeleteView(UbucBaseDeleteView):
    model = EquipmentNote
    success_url = reverse_lazy("equipment-list")