from django.db import models
from kategori.models import Kategori

# Create your models here.
class Artikel(models.Model):
    id_artikel = models.IntegerField(primary_key=True)
    judul = models.CharField(max_length=255)
    word_count = models.IntegerField()
    bluelinks_count = models.IntegerField()
    char_count = models.IntegerField()

    def __str__(self):
        return self.judul
    
class Artikel_Kategori(models.Model):
    id_artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    judul = models.CharField(max_length=255)
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    nama_kategori = models.CharField(max_length=255) 
    subcategories = models.BooleanField(default=None, null=True)

    def __str__(self):
        return f"{self.id_artikel} - {self.nama_kategori}"