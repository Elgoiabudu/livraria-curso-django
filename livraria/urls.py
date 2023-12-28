from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh Token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Verify Token
    path("categorias-class/", views.CategoriaView.as_view()),
    path("categorias-class/<int:id>", views.CategoriaView.as_view()),
    path("categorias-apiview", views.CategoriasList.as_view()),
    path("categorias-apiview/<int:id>/", views.CategoriaDetail.as_view()),
    path("categorias-generic/", views.CategoriasListGeneric.as_view()),
    path("categorias-generic/<int:id>/", views.CategoriaDetailGeneric.as_view()),
    path("", include(router.urls)),
]
