from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from vacancies.models import Vacancy, Skill


class NotInStatusValidator:
    def __init__(self, status_list):
        if not isinstance(status_list, list):
            status_list = [status_list]
        self.status_list = status_list

    def __call__(self, value):
        if value in self.status_list:
            raise serializers.ValidationError(f"Incorrect status.")


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = ["id", "text", "status", "slug", "created", "username", "skills"]


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = "__all__"


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )
    slug = serializers.CharField(max_length=60, validators=[UniqueValidator(queryset=Vacancy.objects.all())])
    status = serializers.CharField(max_length=6, validators=[NotInStatusValidator('close')])
    class Meta:
        model = Vacancy
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):
        self.skills = self.initial_data.pop("skills", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)
        for skill in self.skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)
            vacancy.save()
        return vacancy


class VacancyUpdateSerialiser(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)

    class Meta:
        model = Vacancy
        fields = ["id", "text", "slug", "status", "user", "created", "skills"]

    def is_valid(self, *, raise_exception=False):
        self.skills = self.initial_data.pop("skills", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self.skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)
            vacancy.save()

        return vacancy


class VacancyDestroySerializer(serializers.Serializer):
    class Meta:
        model = Vacancy
        fields = ["id"]
