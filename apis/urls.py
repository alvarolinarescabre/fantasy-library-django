from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import login_required, permission_required
from . import views


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
   openapi.Info(
      title="Fantasy Library API",
      default_version='v1',
      description="Fantasy Library App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alvarolinarescabre@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   generator_class=BothHttpAndHttpsSchemaGenerator,
)


urlpatterns = [
    path('genres/', views.GenreList.as_view(), name='genre_list'),
    path('genres/<int:pk>/', views.GenreDetail.as_view(), name='genre_detail'),
    path('authors/', views.AuthorList.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author_detail'),
    path('books/', views.BookList.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book_detail'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    re_path(r'^swagger/$', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    re_path(r'^redoc/$', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]
