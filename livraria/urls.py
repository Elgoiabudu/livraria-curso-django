from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core import views

from rest_framework_simplejwt.views import ( # Implementação do JWT
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()
router.register(r"autores", views.AutorViewSet)
router.register(r"categorias", views.CategoriaViewSet)
router.register(r"compras", views.CompraViewSet)
router.register(r"editoras", views.EditoraViewSet)
router.register(r"livros", views.LivroViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Autenticação
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh Token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Verify Token
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),    
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Rotas Convencionais da API
    path("categorias-class/", views.CategoriaView.as_view()),
    path("categorias-class/<int:id>", views.CategoriaView.as_view()),
    path("categorias-apiview", views.CategoriasList.as_view()),
    path("categorias-apiview/<int:id>/", views.CategoriaDetail.as_view()),
    path("categorias-generic/", views.CategoriasListGeneric.as_view()),
    path("categorias-generic/<int:id>/", views.CategoriaDetailGeneric.as_view()),
    #Rotas Funcionais distribuidas na API
    path("", include(router.urls)),
]
