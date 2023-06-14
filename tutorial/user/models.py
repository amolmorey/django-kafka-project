from django.db import models


# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    status = models.ForeignKey(
        "Status", related_name="status", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Status(models.Model):
    status_flag = models.IntegerField()
    description = models.CharField(max_length=50)

    class Meta:
        ordering = ["status_flag"]

    def __str__(self):
        return self.description

    @classmethod
    def active(cls):
        return Status.objects.get(status_flag=0)

    @classmethod
    def deleted(cls):
        return Status.objects.get(status_flag=1)
