# Generated by Django 2.1.1 on 2018-10-20 23:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('makeplan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commentid',
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AddField(
            model_name='comment',
            name='datetime',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
        ),
        migrations.AddField(
            model_name='comment',
            name='planid',
            field=models.CharField(default='NULL', max_length=150),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan1',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan2',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan3',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan4',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan5',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan6',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan7',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='planid',
            field=models.CharField(default='default', max_length=150),
        ),
        migrations.AlterField(
            model_name='plans',
            name='shareto',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='submitto',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary1',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary2',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary3',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary4',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary5',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary6',
            field=models.CharField(default='NULL', max_length=500),
        ),
        migrations.AlterField(
            model_name='plans',
            name='summary7',
            field=models.CharField(default='NULL', max_length=500),
        ),
    ]