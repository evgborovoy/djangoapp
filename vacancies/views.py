import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from vacancies.models import Vacancy, Skill


class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        response = []
        for vacancy in self.object_list:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text,
                "slug": vacancy.slug,
            })
        return JsonResponse(response, safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, *args, **kwargs):
        vacancy = self.get_object()
        response = ({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug,
            "created": vacancy.created,
            "user": vacancy.user_id,
            "status": vacancy.status,
        })
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "text", "slug", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)
        vacancy = Vacancy.objects.create(
            user_id=vacancy_data["user_id"],
            text=vacancy_data["text"],
            slug=vacancy_data["slug"],
            status=vacancy_data["status"],
        )

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["text", "slug", "status", "skills"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)
        self.object.text = vacancy_data["text"]
        self.object.slug = vacancy_data["slug"]
        self.object.status = vacancy_data["status"]

        for skill in vacancy_data["skills"]:
            try:
                skill_object = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({"error": "Skill not found"}, status=404)
            self.object.skills.add(skill_object)

        self.object.save()



        return JsonResponse({
            "id": self.object.id,
            "text": self.object.text,
            "slug": self.object.slug,
            "created": self.object.created,
            "user": self.object.user_id,
            "status": self.object.status,
            "skills": list(self.object.skills.all().values_list("name", flat=True))
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
