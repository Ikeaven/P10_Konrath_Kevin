# Generated by Django 3.2.8 on 2021-12-05 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_projet', '0003_auto_20211205_1936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributors',
            old_name='projet',
            new_name='project',
        ),
    ]
