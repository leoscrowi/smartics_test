import uuid

from django.contrib.auth.models import User
from django.db import models

class CategoryEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'category'

    @property
    def creator_id(self):
        if hasattr(self.creator, 'id'):
            return self.creator.id
        if isinstance(self.creator, dict):
            return self.creator.get('id')
        return None