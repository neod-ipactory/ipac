# Generated by Django 3.0.8 on 2020-09-09 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patent', '0004_auto_20200901_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_image', models.ImageField(blank=True, upload_to='media/main')),
                ('sub_image', models.ImageField(blank=True, upload_to='media/sub')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patent.Master')),
            ],
        ),
    ]