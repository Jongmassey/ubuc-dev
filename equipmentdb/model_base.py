from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse_lazy
import re


# abstract base class with common auditing fields
class UbucModel(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True, null=False, editable=False
    )
    updated_on = models.DateTimeField(
        auto_now=True, null=False, editable=False
    )
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

    def save_with_user(self, user) -> None:
        self.updated_by = user
        if self.created_by_id is None:
            self.created_by = user
        return super().save()

    class Meta:
        abstract = True


def classToURL(class_name: str) -> str:
    exp = re.compile("([a-z])([A-Z])")
    return exp.sub(r"\1-\2", class_name).lower()


# Status code enums
class FaultStatus(models.IntegerChoices):
    NEW = 0
    IN_PROGRESS = 1
    FIXED = 2
    UNFIXABLE = 3
    NO_FAULT = 4


class ServiceStatus(models.IntegerChoices):
    UNKNOWN = 0
    IN_SERVICE = 1
    OUT_OF_SERVICE = 2


class TestStatus(models.IntegerChoices):
    UNKNOWN = 0
    IN_TEST = 1
    OUT_OF_TEST = 2
