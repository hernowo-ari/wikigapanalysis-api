# Fungsi untuk mendapatkan konten artikel
import requests
from .models import Artikel, Artikel_Kategori
from kategori.models import Kategori

from django.db import transaction

def get_content(title, language, category, subcategories):
    URL = f"https://{language}.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts|info|links",
        "inprop": "url",
        "pllimit": "max",
        "explaintext": True
    }

    content = ""
    links = []
    char_count = 0

    while True:
        response = requests.get(url=URL, params=PARAMS)
        if response.status_code == 200:
            data = response.json()

            pageid = next(iter(data['query']['pages']))
            page = data['query']['pages'][pageid]

            content = page.get('extract', '')
            char_count = page.get('length', 0)

            if 'links' in page:
                links.extend(page['links'])

            # Check if there is a continuation parameter to fetch more links
            if 'continue' in data:
                PARAMS['plcontinue'] = data['continue']['plcontinue']
            else:
                break  # No more results to fetch
        else:
            return None, "Failed to fetch content"

    word_count = len(content.split())
    links_count = len(links)
    try:
        kategori_obj = Kategori.objects.get(nama_kategori=category, language=language, subcategories=subcategories)
    except Kategori.DoesNotExist:
        return None, "Category does not exist"

    with transaction.atomic():
        artikel_obj, created = Artikel.objects.update_or_create(
            id_artikel=pageid,
            defaults={'judul': title, 'word_count': word_count, 'bluelinks_count': links_count, 'char_count': char_count}
        )

        artikel_kategori_obj, created = Artikel_Kategori.objects.update_or_create(
            id_artikel=artikel_obj,
            nama_kategori=kategori_obj.nama_kategori,
            defaults={'id_kategori': kategori_obj, 'judul': title, 'subcategories': subcategories}
        )
        
    return {
        'pageid': pageid,
        'title': title,
        'word_count': word_count,
        'links_count': links_count,
        'char_count': char_count
    }, None

# try:
        # # Check if the entry exists
        #     artikel_kategori_obj = Artikel_Kategori.objects.filter(id_artikel=artikel_obj, nama_kategori = kategori_obj.nama_kategori)
        #     if len(artikel_kategori_obj) == 0:
        #         Artikel_Kategori.objects.create(id_artikel=artikel_obj, nama_kategori=kategori_obj.nama_kategori, id_kategori = kategori_obj, judul=title, subcategories=subcategories)

        #     for item in artikel_kategori_obj:
        #         if item.subcategories == True and subcategories == False:
        #             item.subcategories = False
        #             item.save()
    
        # except Exception as e:
        #     # Handle any other exceptions
        #     print(f"Error: {e}")
        #     return {'Error': f"{e}"}