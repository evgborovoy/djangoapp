from django.contrib.auth.models import AbstractUser, User
from django.db import models



class User(AbstractUser):
    MALE = "m"
    FEMALE = "f"
    SEX = [(MALE, "Male"), (FEMALE, "FEMALE")]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
