import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from djangoapp import settings
from vacancies.models import Vacancy, Skill


class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        self.object_list = self.object_list.select_related("user").prefetch_related("skills").order_by("text")   # sorting objects on "text" field

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)   # pagination
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies = []
        for vacancy in page_obj:
            vacancies.append({
                "id": vacancy.id,
                "text": vacancy.text,
                "slug": vacancy.slug,
                "created": vacancy.created,
                "username": vacancy.user.username,
                "status": vacancy.status,
                "skills": list(map(str, vacancy.skills.all()))
            })

        response = {
            "items": vacancies,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
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
            "skills": list(map(str, vacancy.skills.all()))
        })
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "text", "slug", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)
        vacancy = Vacancy.objects.create(
            text=vacancy_data["text"],
            slug=vacancy_data["slug"],
            status=vacancy_data["status"],
        )

        vacancy.user = get_object_or_404(User, pk=vacancy_data["user_id"])
        for skill in vacancy_data["skills"]:
            skill_obj, create = Skill.objects.get_or_create(
                name=skill,
                defaults={
                    "is_active": True
                })
            vacancy.skills.add(skill_obj)
            vacancy.save()


        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text,
            "slug": vacancy.slug,
            "status": vacancy.status,
            "created": vacancy.created,
            "user": vacancy.user_id
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


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy'))
        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        users = []
        for user in page_object:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacansies": user.vacancies
            })
        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]
        }

        return JsonResponse(response)