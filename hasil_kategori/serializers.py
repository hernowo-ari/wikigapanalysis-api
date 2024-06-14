from rest_framework import serializers
from .models import Hasil_Kategori

class HasilKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hasil_Kategori
        fields = '__all__'