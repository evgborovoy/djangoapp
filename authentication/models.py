from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    MALE = "m"
    FEMALE = "f"
    SEX = [(MALE, "Male"), (FEMALE, "FEMALE")]

    HR = "hr"
    SEEKER = "seeker"
    UNKNOWN = "unknown"

    ROLE = [(HR, HR), (SEEKER, SEEKER), (UNKNOWN, UNKNOWN)]
    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    role = models.CharField(max_length=7, default=UNKNOWN)
