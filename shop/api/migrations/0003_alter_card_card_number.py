# Generated by Django 5.1.1 on 2024-10-10 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_card_cvv_card_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.CharField(default='', max_length=19),
        ),
    ]
