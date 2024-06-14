from django.db import models
from kategori.models import Kategori

# Create your models here.
class Hasil_Kategori(models.Model):
    id_hasil_kat = models.AutoField(primary_key=True)
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    words_gini_score = models.FloatField(default=None, null=True)
    bluelinks_gini_score = models.FloatField(default=None, null=True)
    char_gini_score = models.FloatField(default=None, null=True)

    words_mean = models.FloatField(default=None, null=True)
    bluelinks_mean = models.FloatField(default=None, null=True)
    char_mean = models.FloatField(default=None, null=True)

    words_median = models.FloatField(default=None, null=True)
    bluelinks_median = models.FloatField(default=None, null=True)
    char_median = models.FloatField(default=None, null=True)

    words_std = models.FloatField(default=None, null=True)
    bluelinks_std = models.FloatField(default=None, null=True)
    char_std = models.FloatField(default=None, null=True)

    def __str__(self):
        return f"{self.id_kategori}"
