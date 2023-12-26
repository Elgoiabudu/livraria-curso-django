from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from core.models import Categoria

import json


@method_decorator(csrf_exempt, name='dispatch')
class CategoriaView(View):
    def get(self, request, id=None):
        if id:
            qs = Categoria.objects.get(id=id)
            data = {}
            data['id'] = qs.id
            data['descricao'] = qs.descricao
            return JsonResponse(data)
        else:
            data = list(Categoria.objects.values())
            formmatted_data = json.dumps(data, ensure_ascii=False)
            return HttpResponse(formmatted_data, content_type='application/json')
    
    def post(self, request):
        json_data = json.loads(request.body)
        new_register = Categoria.objects.create(**json_data)
        data = {"id": new_register.id, "descricao": new_register.descricao}
        return JsonResponse(data)
    
    def patch(self, request, id):
        json_data = json.loads(request.body)
        qs = Categoria.objects.get(id=id)
        qs.descricao = json_data['descricao'] #if 'descricao' is json_data else qs.descricao
        qs.save()
        data = {}
        data['id'] = qs.id
        data['descricao'] = qs.descricao
        return JsonResponse(data)

    def delete(self, request, id):
        try:
            qs = Categoria.objects.get(id=id)
            qs.delete()
            data = {'message': 'Registro excluido com sucesso.'}
            return JsonResponse(data)
        except:
            data = {'message': 'Deleção protegida contra cascateamento.'}
            return JsonResponse(data)

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class CategoriasList(APIView):
    def get(self, request):
        categoria = Categoria.objects.all()
        serializer = CategoriaSerializer(categoria, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetail(APIView):
    def get(self, request, id):
        categoria = get_object_or_404(Categoria.objects.all(), id=id)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    def put(self, request,id):
        categoria = get_object_or_404(Categoria.objects.all(), id=id)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:                    
            categoria = get_object_or_404(Categoria.objects.all(), id=id)
            categoria.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class CategoriasListGeneric(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetailGeneric(RetrieveUpdateDestroyAPIView):    
    lookup_field = 'id'
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer