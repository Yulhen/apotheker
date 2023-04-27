from django.contrib.auth.models import User
from django.db import models


class ManagerMixin:
    objects = models.Manager()


class Drug(models.Model, ManagerMixin):
    name = models.TextField()
    description = models.TextField()


class Receipt(models.Model, ManagerMixin):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='receipts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.IntegerField()


class ReceiptSchedule(models.Model, ManagerMixin):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='schedules')
    time = models.TimeField()
