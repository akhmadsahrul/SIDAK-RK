# Generated by Django 5.1.7 on 2025-03-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidak_app', '0006_alter_anakkaryawan_foto_anak_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anakkaryawan',
            name='status_anak',
            field=models.CharField(max_length=50),
        ),
    ]
