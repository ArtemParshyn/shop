# Generated by Django 5.1.1 on 2024-11-26 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_card_base_alter_card_company_remove_card_bin_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='city',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='state',
            new_name='bank',
        ),
        migrations.AddField(
            model_name='card',
            name='issuingnetwork',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='card',
            name='name',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='expired',
            field=models.CharField(max_length=7),
        ),
        migrations.DeleteModel(
            name='Checked_card',
        ),
    ]