from typing import Dict
from django.db import models
from django.db.models import constraints
from django.db.models.deletion import RESTRICT
from datetime import timedelta, date
from equipmentdb.model_base import UbucModel, ServiceStatus, TestStatus, FaultStatus


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
        if (
            not self.services.exists()
            and not self.equipment_type.equipmenttypeserviceschedule_set.exists()
        ):
            return ServiceStatus.UNKNOWN
        else:
            if self.service_time_remaining < timedelta():
                return ServiceStatus.OUT_OF_SERVICE
        return ServiceStatus.IN_SERVICE

    @property
    def service_time_remaining(self) -> timedelta:
        if (
            not self.services.exists()
            or not self.equipment_type.equipmenttypeserviceschedule_set.exists()
        ):
            return timedelta()
        most_recent_service = self.services.orderby("-date").first().date
        interval = self.equipment_type.equipmenttypeserviceschedule_set.first().interval
        td = date.today() - (most_recent_service + interval)
        return td

    @property
    def fault_status(self) -> FaultStatus:
        fst = self.faults
        if fst.count() >0:
            return FaultStatus(fst.order_by("-created_on").first().status)
        return FaultStatus.NO_FAULT

    @property
    def test_status_formatted(self):
        test_statuses = [(0, "Unknown")]
        if -1 not in self.test_status.keys():
            test_statuses = [
                (ttid, f"{TestType.objects.get(pk=ttid).name} - {t_status.label}")
                for ttid, t_status in self.test_status.items()
            ]
        return test_statuses

    @property
    def test_status(self) -> Dict[int, TestStatus]:
        if (
            not self.tests.exists()
            and not EquipmentTypeTestSchedule.objects.filter(
                equipment_type=self.equipment_type
            ).exists()
        ):
            return {-1: TestStatus.UNKNOWN}
        ret = {}
        for test_schedule in EquipmentTypeTestSchedule.objects.filter(
            equipment_type=self.equipment_type
        ):
            if self.tests.count()==0:
                ret[test_schedule.test_type.id] = TestStatus.OUT_OF_TEST
                continue
            most_recent_test = (
                self.tests.filter(test_type=test_schedule.test_type)
                .orderby("-date")
                .first()
            )
            interval = test_schedule.interval
            td = date.today() - (most_recent_test + interval)
            ret[test_schedule.test_type.id] = TestStatus.OUT_OF_TEST if td<0 else TestStatus.IN_TEST
        return ret

    @property
    def test_time_remaining(self) -> Dict[int, timedelta]:
        if (
            not self.tests.exists()
            or not EquipmentTypeTestSchedule.objects.filter(
                equipment_type=self.equipment_type
            ).exists()
        ):
            return dict()
        ret = {}
        for test_schedule in EquipmentTypeTestSchedule.objects.filter(
            equipment_type=self.equipment_type
        ):
            most_recent_test = (
                self.tests.filter(test_type=test_schedule.test_type)
                .orderby("-date")
                .first()
            )
            interval = test_schedule.interval
            td = date.today() - (most_recent_test + interval)
            ret[test_schedule.test_type.id] = td
        return ret

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

    def __str__(self) -> str:
        return f"{self.equipment_type.name} - {self.name}"


class TestType(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class EquipmentTypeTestSchedule(EquipmentTypeSchedule):
    test_type = models.ForeignKey(
        TestType, null=False, blank=False, on_delete=models.RESTRICT
    )


class EquipmentTypeServiceSchedule(EquipmentTypeSchedule):
    pass


class EquipmentTest(UbucModel):
    equipment = models.ForeignKey(
        Equipment, null=False, on_delete=models.RESTRICT, related_name="tests"
    )
    test_type = models.ForeignKey(TestType, null=False, on_delete=RESTRICT)
    date = models.DateField(null=False, blank=False, auto_now=True)
    passed = models.BooleanField(null=False)
    notes = models.TextField(null=True, blank=True)


class EquipmentService(UbucModel):
    equipment = models.ForeignKey(
        Equipment, null=False, on_delete=models.RESTRICT, related_name="services"
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateField(null=False, blank=False, auto_now=True)
    notes = models.TextField(null=True, blank=True)


class EquipmentFault(UbucModel):
    equipment = models.ForeignKey(
        Equipment, null=False, on_delete=RESTRICT, related_name="faults"
    )
    notes = models.TextField(blank=False, null=False)
    status = models.IntegerField(choices=FaultStatus.choices)
