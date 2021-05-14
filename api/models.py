import datetime
import jwt
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    jwt_token = models.CharField(max_length=255)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.jwt_token = jwt.encode({'id': self.pk, 'exp': str(datetime.datetime.now())}, settings.SECRET_KEY,
                                    algorithm='HS256')
        super().save(*args, **kwargs)

        return self.jwt_token,self.id


class Advisor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    photo = models.TextField()


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
