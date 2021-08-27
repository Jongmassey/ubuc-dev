from typing import Any
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
    template = loader.get_template("equipmentdb/index.html")
    return HttpResponse(template.render())


# base views
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
        self.success_url = self.get_object().get_absolute_url()
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


# equipment items
class EquipmentListView(UbucBaseListView):
    model = Equipment


class EquipmentCreateView(UbucBaseCreateView):
    model = Equipment


class EquipmentUpdateView(UbucBaseUpdateView):
    model = Equipment
    NoteFormSet = inlineformset_factory(
        Equipment, EquipmentNote, fields=("notes",), extra=1
    )
    FaultFormSet = inlineformset_factory(
        Equipment, EquipmentFault, fields=["notes", "status"], extra=1
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        equipment_item = self.get_object()
        form.fields["fault_status"] = forms.CharField(
            initial=equipment_item.fault_status.label, disabled=True, required=False
        )
        form.fields["service_status"] = forms.CharField(
            initial=equipment_item.service_status.label, disabled=True, required=False
        )
        form.fields["service_time_remaining"] = forms.CharField(
            initial=equipment_item.service_time_remaining, disabled=True, required=False
        )

        test_statuses = [(0, "Unknown")]
        if -1 not in equipment_item.test_status.keys():
            test_statuses = [
                (ttid, f"{TestType.objects.get(pk=ttid).name} - {t_status.label}")
                for ttid, t_status in equipment_item.test_status.items()
            ]
        form.fields["test_status"] = forms.MultipleChoiceField(
            disabled=True, required=False, choices=test_statuses
        )

        if "disposed_on" not in form.initial or form.initial["disposed_on"] == None:
            form.fields["disposal_note"].widget.attrs["bsHide"] = "collapse"
            form.fields["disposed_on"].widget.attrs[
                "onChange"
            ] = "enable_disposal_note()"
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        equipment_item = self.get_object()
        notes = self.NoteFormSet(instance=equipment_item)
        faults = self.FaultFormSet(instance=equipment_item)
        ctx["notes"] = notes
        ctx["faults"] = faults
        ctx["equipment_name"] = str(equipment_item)
        return ctx


class EquipmentDeleteView(UbucBaseDeleteView):
    model = Equipment


# Equipment Notes
class EquipmentNoteListView(UbucBaseListView):
    model = EquipmentNote


class EquipmentNoteCreateView(UbucBaseCreateView):
    model = EquipmentNote


class EquipmentNoteUpdateView(UbucBaseUpdateView):
    model = EquipmentNote


class EquipmentNoteDeleteView(UbucBaseDeleteView):
    model = EquipmentNote


# Service Schedules
class EquipmentTypeServiceScheduleListView(UbucBaseListView):
    model = EquipmentTypeServiceSchedule

class EquipmentTypeServiceScheduleCreateView(UbucBaseCreateView):
    model = EquipmentTypeServiceSchedule

class EquipmentTypeServiceScheduleUpdateView(UbucBaseUpdateView):
    model = EquipmentTypeServiceSchedule

class EquipmentTypeServiceScheduleDeleteView(UbucBaseDeleteView):
    model = EquipmentTypeServiceSchedule