# Generated by Django 5.1.1 on 2024-11-08 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_card_cvv_checked_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='checked_card',
            name='code',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
    ]
