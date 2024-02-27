from django.db import models


class TimestampedCreatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimestampedModifiedModel(models.Model):
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimestampedModel(TimestampedCreatedModel, TimestampedModifiedModel):
    class Meta:
        abstract = True
