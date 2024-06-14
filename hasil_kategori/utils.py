from pygini import gini
import numpy as np
from .models import Hasil_Kategori
from kategori.models import Kategori
from artikel.models import Artikel

from django.db.models import Avg, StdDev

def calculate_statistics_for_kategori(kategori_obj):
    try:
        kategori = Kategori.objects.get(id=kategori_obj)
    except Kategori.DoesNotExist:
        return {"Error: Kategori Does Not Exist"}

    if kategori.subcategories:
        articles = Artikel.objects.filter(artikel_kategori__nama_kategori=kategori.nama_kategori)
    else:
        articles = Artikel.objects.filter(artikel_kategori__nama_kategori=kategori.nama_kategori, artikel_kategori__subcategories=False)

    if articles.exists():
        word_counts = np.array(list(articles.values_list('word_count', flat=True)), dtype=np.float64)
        bluelinks_counts = np.array(list(articles.values_list('bluelinks_count', flat=True)), dtype=np.float64)
        char_counts = np.array(list(articles.values_list('char_count', flat=True)), dtype=np.float64)

        words_gini_score = gini(word_counts)
        bluelinks_gini_score = gini(bluelinks_counts)
        char_gini_score = gini(char_counts)

        avg_words = articles.aggregate(avg_words=Avg('word_count'))['avg_words']
        avg_bluelinks = articles.aggregate(avg_bluelinks=Avg('bluelinks_count'))['avg_bluelinks']
        avg_char = articles.aggregate(avg_char=Avg('char_count'))['avg_char']

        median_words = np.median(word_counts)
        median_bluelinks = np.median(bluelinks_counts)
        median_char = np.median(char_counts)

        std_dev_words = articles.aggregate(std_dev_words=StdDev('word_count'))['std_dev_words']
        std_dev_bluelinks = articles.aggregate(std_dev_bluelinks=StdDev('bluelinks_count'))['std_dev_bluelinks']
        std_dev_char = articles.aggregate(std_dev_char=StdDev('char_count'))['std_dev_char']

        try:
            hasil_kategori_obj = Hasil_Kategori.objects.get(id_kategori=kategori)
        except Hasil_Kategori.DoesNotExist:
            # If no Hasil_Kategori object exists, create a new one
            hasil_kategori_obj = Hasil_Kategori.objects.create(id_kategori=kategori)

        hasil_kategori_obj.words_gini_score = words_gini_score
        hasil_kategori_obj.bluelinks_gini_score = bluelinks_gini_score
        hasil_kategori_obj.char_gini_score = char_gini_score

        hasil_kategori_obj.words_mean = avg_words
        hasil_kategori_obj.bluelinks_mean = avg_bluelinks
        hasil_kategori_obj.char_mean = avg_char

        hasil_kategori_obj.words_median = median_words
        hasil_kategori_obj.bluelinks_median = median_bluelinks
        hasil_kategori_obj.char_median = median_char

        hasil_kategori_obj.words_std = std_dev_words
        hasil_kategori_obj.bluelinks_std = std_dev_bluelinks
        hasil_kategori_obj.char_std = std_dev_char

        # Save the updated Hasil_Kategori object
        hasil_kategori_obj.save()
        
        return hasil_kategori_obj
    else:
        raise ValueError(f"No articles found for category '{kategori.nama_kategori}'.")