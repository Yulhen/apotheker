# Generated by Django 4.2 on 2023-05-01 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_receipt_amount_remove_receipt_times_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='start_dt',
            field=models.DateField(default='2023-05-01'),
            preserve_default=False,
        ),
    ]