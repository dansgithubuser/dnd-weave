# Generated by Django 2.1.7 on 2019-03-25 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnd_weave_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='secret',
            name='name',
            field=models.TextField(null=True),
        ),
    ]