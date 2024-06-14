from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import  Hasil_Kategori
from kategori.models import Kategori
from .serializers import HasilKategoriSerializer 
from .utils import calculate_statistics_for_kategori
import urllib.parse

# Create your views here.
class HasilKategoriViewSet(viewsets.ViewSet):
    def list(self, request):
        # Get the value of the query parameter 'kategori'
        nama_kategori = request.query_params.get('kategori')
        subcategories = request.query_params.get('subcategories')

        if not nama_kategori or not subcategories:
            return Response({"error": "kategori and subcategories parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        nama_kategori = urllib.parse.unquote(nama_kategori)
        subcategories = True if subcategories == 'true' else False
        try:
            kategori_obj = Kategori.objects.get(nama_kategori=nama_kategori, subcategories=subcategories)
            hasil_kategori_obj = calculate_statistics_for_kategori(kategori_obj.pk)
            
            #If Kategori subcategory created/updated, Kategori non subcategory also updated
            if kategori_obj.subcategories == True:
                try:
                    kategori_obj_2 = Kategori.objects.get(nama_kategori=nama_kategori, subcategories=False)
                    hasil_kategori_obj = calculate_statistics_for_kategori(kategori_obj_2.pk)
                except Kategori.DoesNotExist:
                    return Response({"error": f"Kategori with name '{nama_kategori}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
                
            queryset = Hasil_Kategori.objects.get(id_kategori=kategori_obj)
        except Kategori.DoesNotExist:
            return Response({"error": f"Kategori with name '{nama_kategori}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = HasilKategoriSerializer(queryset)
        return Response(serializer.data)
        
class HasilKategoriDatabaseView(APIView):
    def get(self, request):
        category_name = request.query_params.get('kategori')
        subcategories = request.query_params.get('subcategories')

        if not category_name or not subcategories:
            return Response({"error": "kategori and subcategories parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        nama_kategori = urllib.parse.unquote(category_name)
        subcategories = True if subcategories.lower() == 'true' else False

        try:
            kategori_obj = Kategori.objects.get(nama_kategori=nama_kategori, subcategories=subcategories)
            queryset = Hasil_Kategori.objects.get(id_kategori=kategori_obj)
        except Kategori.DoesNotExist:
            return Response({"error": f"Kategori with name '{nama_kategori}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Hasil_Kategori.DoesNotExist:
            return Response({"error": f"Hasil Kategori with name '{nama_kategori}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HasilKategoriSerializer(queryset)
        return Response(serializer.data)
    