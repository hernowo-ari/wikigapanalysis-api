from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Kategori
from .serializers import KategoriSerializer
from .utils import get_categories, search_wikipedia_categories
import urllib.parse

# Create your views here.
class KategoriViewSet(viewsets.ViewSet):
    serializer_class = KategoriSerializer

    def list(self, request):
        category_name = request.query_params.get('kategori')
        language = request.query_params.get('language')
        flag = request.query_params.get('subcategories')

        if not category_name or not language or not flag:
            return Response({"error": "kategori and language and subcategories parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        flag = True if flag == 'true' else False
        nama_kategori = search_wikipedia_categories(category_name, language)
        page_titles, page_titles_sub = get_categories(nama_kategori, language, flag)
        queryset = Kategori.objects.get(nama_kategori=nama_kategori, language=language, subcategories=flag)
        serializer = KategoriSerializer(queryset)
        return Response({"categories": serializer.data, "page_titles": page_titles, "page_titles_sub": page_titles_sub})


class KategoriDatabaseView(APIView):
    def get(self, request):
        category_name = request.query_params.get('kategori')
        language = request.query_params.get('language')
        flag = request.query_params.get('subcategories')

        if not category_name or not language or not flag:
            return Response({"error": "kategori, language, and subcategories parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        nama_kategori = urllib.parse.unquote(category_name)
        flag = True if flag.lower() == 'true' else False

        try:
            queryset = Kategori.objects.get(nama_kategori=nama_kategori, language=language, subcategories=flag)
        except Kategori.DoesNotExist:
            return Response({"error": f"Kategori with name '{nama_kategori}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = KategoriSerializer(queryset)
        return Response(serializer.data)