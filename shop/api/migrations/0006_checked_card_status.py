# Generated by Django 5.1.1 on 2024-11-12 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_checked_card_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='checked_card',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
