from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        abstract = True

