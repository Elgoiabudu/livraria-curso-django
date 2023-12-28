from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from rest_framework import serializers

from core.models import Categoria, Editora, Autor, Livro, Compra, ItensCompra


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class EditoraSerializer(ModelSerializer):  # Retorna o nome e id da editora
    class Meta:
        model = Editora
        fields = "__all__"


class EditoraNestedSerializer(ModelSerializer):  # Somente o nome da editora
    class Meta:
        model = Editora
        fields = ("nome",)


class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = "__all__"


class LivroSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = "__all__"


class LivroDetailSerializer(ModelSerializer):
    categoria = CharField(source="categoria.descricao")
    editora = EditoraNestedSerializer()
    # autores = SerializerMethodField() - Com essa adaptação, é retornado apenas o nome do(s) autor(es)

    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1  # Exibe um nível a mais no rsponse.

    def get_autores(self, instance):
        nomes_autores = []
        autores = instance.autores.get_queryset()
        for autor in autores:
            nomes_autores.append(autor.nome)
        return nomes_autores


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 2

    def get_total(self, instance):
        return instance.quantidade * instance.livro.preco


class CriarEditarItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")


class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email")
    status = SerializerMethodField()
    itens = ItensCompraSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("id", "status", "usuario", "itens", "total")

    def get_status(self, instance):
        return instance.get_status_display()


class CriarEditarCompraSerializer(ModelSerializer):
    itens = CriarEditarItensCompraSerializer(many=True)
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Capturando a instancia para identificar o usuário

    class Meta:
        model = Compra
        fields = ("id", "usuario", "itens")

    def create(self, validate_data):        
        itens = validate_data.pop("itens")
        compra = Compra.objects.create(**validate_data)
        for item in itens:
            ItensCompra.objects.create(compra=compra, **item)        
        compra.save()
        return compra

    def update(self, instance, validated_data):
        itens = validated_data.pop("itens")
        if itens:
            instance.itens.all().delete()
            for item in itens:
                ItensCompra.objects.create(compra=instance, **item)
            instance.save()
        return instance
