# Generated by Django 2.1.1 on 2018-10-17 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('commentid', models.CharField(max_length=150)),
                ('content', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='plans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('planid', models.CharField(max_length=150)),
                ('datetime', models.CharField(default=django.utils.timezone.now, max_length=100)),
                ('plan1', models.CharField(max_length=500)),
                ('plan2', models.CharField(max_length=500)),
                ('plan3', models.CharField(max_length=500)),
                ('plan4', models.CharField(max_length=500)),
                ('plan5', models.CharField(max_length=500)),
                ('plan6', models.CharField(max_length=500)),
                ('plan7', models.CharField(max_length=500)),
                ('summary1', models.CharField(max_length=500)),
                ('summary2', models.CharField(max_length=500)),
                ('summary3', models.CharField(max_length=500)),
                ('summary4', models.CharField(max_length=500)),
                ('summary5', models.CharField(max_length=500)),
                ('summary6', models.CharField(max_length=500)),
                ('summary7', models.CharField(max_length=500)),
                ('shareto', models.CharField(max_length=500)),
                ('submitto', models.CharField(max_length=500)),
            ],
        ),
    ]
