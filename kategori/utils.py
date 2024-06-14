import requests
from .models import Kategori
from django.utils import timezone


def get_categories(category, language, subcategories_flag):
    base_url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "format": "json",
        "cmlimit": "500"
    }

    non_subcategory_titles = set()
    subcategory_titles = set()
    subcategories_to_process = []

    while True:
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if "query" in data and "categorymembers" in data["query"]:
                for member in data["query"]["categorymembers"]:
                    title = member["title"]
                    ns = member["ns"]
                    if ns == 0:
                        non_subcategory_titles.add(title)
                    elif subcategories_flag and ns == 14:
                        subcategories_to_process.append(title)

                if 'continue' in data:
                    params['cmcontinue'] = data['continue']['cmcontinue']
                else:
                    break
            else:
                return list(non_subcategory_titles), list(subcategory_titles)
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return list(non_subcategory_titles), list(subcategory_titles)

    for subcategory in subcategories_to_process:
        subcategory_params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": subcategory,
            "format": "json",
            "cmlimit": "500"
        }
        while True:
            sub_response = requests.get(base_url, params=subcategory_params)

            if sub_response.status_code == 200:
                sub_data = sub_response.json()
                if "query" in sub_data and "categorymembers" in sub_data["query"]:
                    for member in sub_data["query"]["categorymembers"]:
                        title = member["title"]
                        ns = member["ns"]
                        if ns == 0:
                            subcategory_titles.add(title)

                    if 'continue' in sub_data:
                        subcategory_params['cmcontinue'] = sub_data['continue']['cmcontinue']
                    else:
                        break
            else:
                print(f"Error: API request failed with status code {sub_response.status_code}")
                break

    try:
        kategori_obj = Kategori.objects.get(nama_kategori=category, language=language, subcategories=subcategories_flag)
        kategori_obj.member_count = len(non_subcategory_titles) + len(subcategory_titles)
        kategori_obj.created_at = timezone.localtime(timezone.now(), timezone.get_fixed_timezone(420))
        kategori_obj.save()

        #If Kategori subcategory created/updated, Kategori non subcategory also updated
        if kategori_obj.subcategories == True:
            try:
                kategori_obj_2 = Kategori.objects.get(nama_kategori=category, language=language, subcategories=False)
                kategori_obj_2.created_at = timezone.localtime(timezone.now(), timezone.get_fixed_timezone(420))
                kategori_obj_2.save()
            except Kategori.DoesNotExist:
                kategori_obj_2 = Kategori.objects.create(nama_kategori=category, language=language, subcategories=False, member_count=len(non_subcategory_titles))

    except Kategori.DoesNotExist:
        kategori_obj = Kategori.objects.create(nama_kategori=category, language=language, subcategories=subcategories_flag, member_count=len(non_subcategory_titles) + len(subcategory_titles))
        if kategori_obj.subcategories == True:
            kategori_obj_2 = Kategori.objects.update_or_create(nama_kategori=category, language=language, subcategories=False, member_count=len(non_subcategory_titles))
    except Exception as e:
        print(f"Error: {e}")
        return {'Error': f"{e}"}

    return list(non_subcategory_titles), list(subcategory_titles)


def search_wikipedia_categories(search_query, language):
    url = f"https://{language}.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_query}&srnamespace=14&&srlimit=1&format=json"
    response = requests.get(url)
    categories = []

    if response.status_code == 200:
        data = response.json()
        if "query" in data and "search" in data["query"]:
            for result in data["query"]["search"]:
                categories.append(result["title"][9:])

    return categories[0]