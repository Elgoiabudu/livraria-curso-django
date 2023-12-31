from django.http import HttpResponse, JsonResponse

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.models import Categoria

import json


@method_decorator(csrf_exempt, name="dispatch")
class CategoriaView(View):
    def get(self, request, id=None):
        if id:
            qs = Categoria.objects.get(id=id)
            data = {}
            data["id"] = qs.id
            data["descricao"] = qs.descricao
            return JsonResponse(data)
        else:
            data = list(Categoria.objects.values())
            formmatted_data = json.dumps(data, ensure_ascii=False)
            return HttpResponse(formmatted_data, content_type="application/json")

    def post(self, request):
        json_data = json.loads(request.body)
        new_register = Categoria.objects.create(**json_data)
        data = {"id": new_register.id, "descricao": new_register.descricao}
        return JsonResponse(data)

    def patch(self, request, id):
        json_data = json.loads(request.body)
        qs = Categoria.objects.get(id=id)
        qs.descricao = json_data[
            "descricao"
        ]  # if 'descricao' is json_data else qs.descricao
        qs.save()
        data = {}
        data["id"] = qs.id
        data["descricao"] = qs.descricao
        return JsonResponse(data)

    def delete(self, request, id):
        try:
            qs = Categoria.objects.get(id=id)
            qs.delete()
            data = {"message": "Registro excluido com sucesso."}
            return JsonResponse(data)
        except:
            data = {"message": "Deleção protegida contra cascateamento."}
            return JsonResponse(data)