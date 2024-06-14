from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Artikel
from kategori.models import Kategori
from .serializers import ArtikelSerializer 

from .utils import get_content
from kategori.utils import get_categories
import urllib.parse

# Create your views here.
class ArticleContentView(APIView):

    def get(self, request):
        title = request.query_params.get('title')
        language = request.query_params.get('language')
        category = request.query_params.get('kategori')
        subcategories = request.query_params.get('subcategories')
        
        category = urllib.parse.unquote(category)
        title = urllib.parse.unquote(title)
        subcategories = True if subcategories == 'true' else False
        if not title or not language or not category:
            return Response({"error": "title, language, subcategories, and kategori parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        content_data, error = get_content(title, language, category, subcategories)

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(content_data)
    

class ArtikelByKategoriViewSet(viewsets.ViewSet):
    def list(self, request):
        kategori = request.GET.get('kategori')
        language = request.query_params.get('language')
        flag = request.GET.get('subcategories')

        kategori = urllib.parse.unquote(kategori)
        if not kategori or not language or flag not in {'true', 'false'}:
            return Response({"error": "kategori, language, and valid flag parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            kategori = Kategori.objects.filter(nama_kategori=kategori).first()
        except Kategori.DoesNotExist:
            raise ValueError(f"Kategori with name '{kategori}' does not exist.")
        
        if flag == 'false':
            artikel_queryset = Artikel.objects.filter(artikel_kategori__nama_kategori=kategori.nama_kategori, artikel_kategori__subcategories=False)
        else:
            # Fetch articles from the main category only
            artikel_queryset = Artikel.objects.filter(artikel_kategori__nama_kategori=kategori.nama_kategori)

        serializer = ArtikelSerializer(artikel_queryset, many=True)
        return Response(serializer.data)