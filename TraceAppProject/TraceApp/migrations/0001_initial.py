# Generated by Django 3.1 on 2020-08-19 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trace',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('trace', models.TextField()),
            ],
        ),
    ]
