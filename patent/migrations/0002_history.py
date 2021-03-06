# Generated by Django 3.0.8 on 2020-09-01 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicationNumber', models.CharField(max_length=200)),
                ('documentNumber', models.CharField(max_length=200)),
                ('documentDate', models.CharField(max_length=200)),
                ('documentTitle', models.CharField(max_length=200)),
                ('documentTitleEng', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('StatusEng', models.CharField(max_length=200)),
                ('step', models.CharField(max_length=200)),
                ('trialNumber', models.CharField(max_length=200)),
                ('registrationNumber', models.CharField(max_length=200)),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patent.Master')),
            ],
            options={
                'db_table': 'histories',
            },
        ),
    ]
