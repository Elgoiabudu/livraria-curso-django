from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

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


class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email")
    status = SerializerMethodField()
    itens = ItensCompraSerializer(many=True)

    class Meta:
        model = Compra
        fields = "__all__"

    def get_status(self, instance):
        return instance.get_status_display()
