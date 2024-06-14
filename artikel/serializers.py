from rest_framework import serializers
from .models import Artikel, Artikel_Kategori

class ArtikelSerializer(serializers.ModelSerializer):
    nama_kategori = serializers.SerializerMethodField()

    class Meta:
        model = Artikel
        fields = ['judul', 'word_count', 'bluelinks_count', 'char_count', 'nama_kategori']

    def get_nama_kategori(self, obj):
        # Get the related Artikel_Kategori instance
        artikel_kategori_instance = Artikel_Kategori.objects.filter(id_artikel=obj.id_artikel).first()
        if artikel_kategori_instance:
            return artikel_kategori_instance.nama_kategori
        else:
            return None