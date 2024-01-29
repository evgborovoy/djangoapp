import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


def hello(request):
    return HttpResponse("Hello world")


@method_decorator(csrf_exempt, name="dispatch")
class VacancyView(View):

    def get(self, request):

        if request.method == "GET":
            vacancies = Vacancy.objects.all()
            search_text = request.GET.get("text", None)
            if search_text:
                vacancies = vacancies.filter(text=search_text)

            response = []
            for vacancy in vacancies:
                response.append({
                    "id": vacancy.id,
                    "text": vacancy.text,
                    "slug": vacancy.slug,
                })
            return JsonResponse(response, safe=False)

    def post(self, request):
        vacancy_data = json.loads(request.body)
        vacancy = Vacancy()
        vacancy.text = vacancy_data["text"]
        vacancy.slug = vacancy_data["slug"]
        vacancy.save()
        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug
        })


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, *args, **kwargs):
        vacancy = self.get_object()
        response = ({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug
        })
        return JsonResponse(response, safe=False)
