from django import forms
from django.forms.models import BaseInlineFormSet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models.fields import DateField
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DateInput(forms.DateInput):
    input_type = "date"


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


class UbucInlineFormSet(BaseInlineFormSet):
    def save(self, user):
        objs = super().save(commit=False)
        for obj in objs:
            obj.save_with_user(user=user)
        for delobj in self.deleted_objects:
            delobj.delete()
