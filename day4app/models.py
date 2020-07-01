from django.db import models

# Create your models here.
# from bookapp.models import BaseModel


class User(models.Model):
    gender_choices = (
        (0,'female'),
        (1,'male'),
        (2,'unknown')
    )
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=11)
    gender = models.SmallIntegerField(choices=gender_choices,default=1)
    is_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = "excise_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
