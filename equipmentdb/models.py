from django.db import models
from django.db.models import constraints
from django.contrib.auth.models import User


class UbucModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)
    created_by = models.ForeignKey(User, null=False,blank=False,on_delete=models.RESTRICT,related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(User, null=False,blank=False,on_delete=models.RESTRICT,related_name='%(class)s_updated_by')
    class Meta:
        abstract = True

class EquipmentType(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)

class Equipment(UbucModel):
    acquired_on = models.DateField(null=False,blank=False)
    disposed_on = models.DateField(null=True,blank=True)
    disposal_note = models.TextField(null=True,blank=True)
    equipment_type = models.ForeignKey(EquipmentType, null=False,on_delete=models.RESTRICT)
    ubuc_id = models.IntegerField(null=False,blank=False)
    description = models.TextField(null=False,blank=False)
    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=["equipment_type","ubuc_id"], name="unique_ubuc_id")
        ]

class EquipmentNote(UbucModel):
    equipment = models.ForeignKey(Equipment, null=False,on_delete=models.RESTRICT)
    notes = models.TextField(null=True,blank=True)

class Test(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)

class Service(UbucModel):
    name = models.CharField(max_length=255, null=False, blank=False)

class EquipmentTypeSchedule(UbucModel):
    equipment_type = models.ForeignKey(EquipmentType, null=False,blank=False,on_delete=models.RESTRICT)
    mandatory = models.BooleanField(null=False,blank=False)
    interval = models.DurationField(null=False,blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False,blank=False)
    class Meta:
        abstract = True

class EquipmentTypeTestSchedule(EquipmentTypeSchedule): 
    test = models.ForeignKey(Test,null=False,blank=False,on_delete=models.RESTRICT)

class EquipmentTypeServiceSchedule(EquipmentTypeSchedule):
    service = models.ForeignKey(Service,null=False,blank=False,on_delete=models.RESTRICT)

class EquipmentTest(UbucModel):
    equipment = models.ForeignKey(Equipment, null=False,on_delete=models.RESTRICT)

class EquipmentService(UbucModel):
    equipment = models.ForeignKey(Equipment, null=False,on_delete=models.RESTRICT)