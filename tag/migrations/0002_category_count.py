# Generated by Django 3.0.8 on 2020-09-07 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='count',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
