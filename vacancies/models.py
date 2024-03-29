from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from authentication.models import User


def updated_date(value):
    if value < date.today():
        raise ValidationError(f"date {value} in the past")

class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Навык"          # Для написания по-русски в админке в ед.числе
        verbose_name_plural = "Навыки"  # Для написания по-русски в админке в мн.числе

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрыта")
    ]
    slug = models.SlugField(max_length=60)
    text = models.CharField(max_length=1500)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skill)

    likes = models.IntegerField(default=0)
    min_experience = models.IntegerField(null=True, validators=([MinValueValidator(0)]))
    updated_at = models.DateField(null=True, validators=[updated_date])

    class Meta:
        verbose_name = "Вакансия"          # Для написания по-русски в админке в ед.числе
        verbose_name_plural = "Вакансии"   # Для написания по-русски в админке в мн.числе

    def __str__(self):
        return self.slug
    @property
    def username(self):
        return self.user.username if self.user else None
