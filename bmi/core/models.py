from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedCreatedModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        abstract = True


class TimestampedModifiedModel(models.Model):
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class TimestampedModel(TimestampedCreatedModel, TimestampedModifiedModel):
    class Meta:
        abstract = True


class NameModel(models.Model):
    name = models.CharField(
        _('name'), max_length=128
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name
