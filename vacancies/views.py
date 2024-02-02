import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from djangoapp import settings
from vacancies.models import Vacancy, Skill
from vacancies.serialaizer import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerialiser, VacancyDestroySerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    fields = ["user", "text", "slug", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
        if vacancy_data.is_valid():
            vacancy_data.save()
        else:
            return JsonResponse(vacancy_data.errors)

        return JsonResponse(vacancy_data.data)


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerialiser


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy
    serializer_class = VacancyDestroySerializer


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count("vacancy"))
        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        users = []
        for user in page_object:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies
            })
        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg("vacancies"))["avg"]
        }

        return JsonResponse(response)
