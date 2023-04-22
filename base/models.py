from django.db import models
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True