from django.db import models
from django.utils import timezone

class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(420)))
    language = models.CharField(max_length=255)
    member_count = models.IntegerField()
    subcategories = models.BooleanField(default=None, null=True)
    
    def __str__(self):
        return self.nama_kategori