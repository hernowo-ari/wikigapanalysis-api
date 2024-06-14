"""
URL configuration for wikigapanalysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from kategori.views import KategoriViewSet, KategoriDatabaseView
from artikel.views import ArtikelByKategoriViewSet, ArticleContentView
from hasil_kategori.views import HasilKategoriViewSet, HasilKategoriDatabaseView

router = routers.DefaultRouter()
router.register(r'kategori', KategoriViewSet, basename='kategori')
router.register(r'hasil_kategori', HasilKategoriViewSet, basename='hasil-kategori')
router.register(r'artikel', ArtikelByKategoriViewSet, basename='artikel')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/schema/', SpectacularAPIView.as_view() , name="schema"),
    # path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('artikel/get/', ArticleContentView.as_view(), name='article-content'),
    path('kategori/get/', KategoriDatabaseView.as_view(), name='kategori-database'),
    path('hasil_kategori/get/', HasilKategoriDatabaseView.as_view(), name='hasil-kategori-database'),
]

urlpatterns += router.urls
