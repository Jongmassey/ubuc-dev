from equipmentdb.models import EquipmentType
from equipmentdb.models import *
from equipmentdb.view_base import (
    UbucBaseCreateView,
    UbucBaseListView,
    UbucBaseDeleteView,
    UbucBaseUpdateView,
    UbucInlineFormSet
)
from django import forms
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.template import loader
from django.db import transaction


def index(request):
    template = loader.get_template("equipmentdb/index.html")
    return HttpResponse(template.render())


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
        Equipment, EquipmentNote, fields=("notes",), extra=1,formset=UbucInlineFormSet
    )
    FaultFormSet = inlineformset_factory(
        Equipment, EquipmentFault, fields=["notes", "status"], extra=1, can_delete= False,formset=UbucInlineFormSet
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
        if self.request.POST:
            notes = self.NoteFormSet(self.request.POST, instance=equipment_item)
            faults = self.FaultFormSet(self.request.POST, instance=equipment_item)
        else:
            notes = self.NoteFormSet(instance=equipment_item)
            faults = self.FaultFormSet(instance=equipment_item)
        ctx["notes"] = notes
        ctx["faults"] = faults
        ctx["equipment_name"] = str(equipment_item)
        
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        notes = context['notes']
        faults = context['faults']
        with transaction.atomic():
            self.object = form.save()
            if notes.is_valid():
                notes.save(self.request.user)
            else:
                raise ValueError (f""" notes form did not validate:

                {notes.errors}
                """)
            if faults.is_valid():
                faults.save(self.request.user)
            else:
                raise ValueError(f""" faults form did not validate:
                
                {faults.errors}
                """)
        return super(EquipmentUpdateView,self).form_valid(form)

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


# Test Schedules
class EquipmentTypeTestScheduleListView(UbucBaseListView):
    model = EquipmentTypeTestSchedule


class EquipmentTypeTestScheduleCreateView(UbucBaseCreateView):
    model = EquipmentTypeTestSchedule


class EquipmentTypeTestScheduleUpdateView(UbucBaseUpdateView):
    model = EquipmentTypeTestSchedule


class EquipmentTypeTestScheduleDeleteView(UbucBaseDeleteView):
    model = EquipmentTypeTestSchedule


# Test Types
class TestTypeListView(UbucBaseListView):
    model = TestType


class TestTypeCreateView(UbucBaseCreateView):
    model = TestType


class TestTypeUpdateView(UbucBaseUpdateView):
    model = TestType


class TestTypeDeleteView(UbucBaseDeleteView):
    model = TestType
