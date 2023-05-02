from datetime import datetime, time, timedelta

from django.contrib.auth.models import User
from django.db import models


class ManagerMixin:
    objects = models.Manager()


class Drug(models.Model, ManagerMixin):
    name = models.TextField()
    description = models.TextField()

    def __repr__(self) -> str:
        return str(self.name)


class Receipt(models.Model, ManagerMixin):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='receipts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.IntegerField()
    start_dt = models.DateField()

    @property
    def end_dt(self) -> datetime:
        return self.start_dt + timedelta(days=self.days - 1)

    @property
    def closest_medication(self) -> 'ReceiptSchedule':
        now = datetime.now()
        schedules = self.schedules.order_by('time')
        for schedule in schedules:
            if datetime.combine(now.date(), now.time()) > datetime.combine(now.date(), schedule.time):
                return schedule
        return schedules.first()

    def __repr__(self) -> str:
        return f'{self.drug.name}, {self.user.username}'


class ReceiptSchedule(models.Model, ManagerMixin):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='schedules')
    time = models.TimeField()
    amount = models.IntegerField()
