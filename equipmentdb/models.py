from django.db import models
from django.db.models import constraints
from django.contrib.auth.models import User
from django.db.models.deletion import RESTRICT
from django.urls import reverse_lazy
from datetime import timedelta,date
import re


def classToURL(class_name: str) -> str:
    exp = re.compile("([a-z])([A-Z])")
    return exp.sub(r"\1-\2", class_name).lower()


class FaultStatus(models.IntegerChoices):
    NEW = 0
    IN_PROGRESS = 1
    FIXED = 2
    UNFIXABLE = 3
    NO_FAULT = 4


# Tri-state boolean
class ServiceStatus(models.IntegerChoices):
    UNKNOWN = 0
    IN_SERVICE = 1
    OUT_OF_SERVICE = 2


### abstract base class with common auditing fields
class UbucModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=False, editable=False)
    updated_on = models.DateTimeField(auto_now=True, null=False, editable=False)
    created_by = models.ForeignKey(
        User,
        null=False,
        blank=False,
        editable=False,
        on_delete=models.RESTRICT,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        null=False,
        blank=False,
        editable=False,
        on_delete=models.RESTRICT,
        related_name="%(class)s_updated_by",
    )

    def get_absolute_url(self):
        return reverse_lazy(f"{classToURL(self.__class__.__name__)}-list")

    class Meta:
        abstract = True


class EquipmentType(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=["name"], name="unique_name")
        ]


class Equipment(UbucModel):
    acquired_on = models.DateField(null=False, blank=False)
    disposed_on = models.DateField(null=True, blank=True)
    disposal_note = models.TextField(null=True, blank=True)
    equipment_type = models.ForeignKey(
        EquipmentType, null=False, on_delete=models.RESTRICT
    )
    ubuc_id = models.IntegerField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    @property
    def service_status(self) -> ServiceStatus:
        if not self.services.exists() and self.equipment_type.equipmenttypeserviceschedule_set.exists():
            return ServiceStatus.UNKNOWN
        return ServiceStatus.IN_SERVICE

    @property
    def service_time_remaining(self) -> models.DurationField:
        if not self.services.exists() or not self.equipment_type.equipmenttypeserviceschedule_set.exists():
            return models.DurationField(default=timedelta())
        most_recent_service = self.services.orderby('-date').first().date
        interval = self.equipment_type.equipmenttypeserviceschedule_set.first().interval
        td = date.today() - (most_recent_service+interval)
        return models.DurationField(default=td)
        

    @property
    def fault_status(self) -> FaultStatus:
        return self.faults.order_by('-created_on').first() or FaultStatus.NO_FAULT

    class Meta:
        constraints = [
            constraints.UniqueConstraint(
                fields=["equipment_type", "ubuc_id"], name="unique_ubuc_id"
            )
        ]

    def __str__(self):
        return f"{self.equipment_type} {self.ubuc_id}"


class EquipmentNote(UbucModel):
    equipment = models.ForeignKey(Equipment, null=False, on_delete=models.RESTRICT)
    notes = models.TextField(null=True, blank=True)


class Test(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)


class Service(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateField(null=False,blank=False,auto_now=True)
    notes = models.TextField(null=True,blank=True)


class EquipmentTypeSchedule(UbucModel):
    equipment_type = models.ForeignKey(
        EquipmentType, null=False, blank=False, on_delete=models.RESTRICT
    )
    mandatory = models.BooleanField(null=False, blank=False)
    interval = models.DurationField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    class Meta:
        abstract = True


class EquipmentTypeTestSchedule(EquipmentTypeSchedule):
    test = models.ForeignKey(Test, null=False, blank=False, on_delete=models.RESTRICT)


class EquipmentTypeServiceSchedule(EquipmentTypeSchedule):
    service = models.ForeignKey(
        Service, null=False, blank=False, on_delete=models.RESTRICT
    )

class EquipmentTest(UbucModel):
    equipment = models.ForeignKey(Equipment, null=False, on_delete=models.RESTRICT)


class EquipmentService(UbucModel):
    equipment = models.ForeignKey(Equipment, null=False, on_delete=models.RESTRICT,related_name='services')


class EquipmentFault(UbucModel):
    equipment = models.ForeignKey(
        Equipment, null=False, on_delete=RESTRICT, related_name="faults"
    )
    notes = models.TextField(blank=False, null=False)
    status = models.IntegerField(choices=FaultStatus.choices)
