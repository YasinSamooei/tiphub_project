# Generated by Django 3.2.12 on 2022-08-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_video_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(choices=[('p', 'منتشر شده'), ('i', 'در حال بررسی'), ('b', 'برگشت داده شده')], max_length=1, verbose_name='وضعیت'),
        ),
    ]
