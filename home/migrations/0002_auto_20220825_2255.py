# Generated by Django 3.2.12 on 2022-08-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='آدرس دسته\u200cبندی'),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.BooleanField(default=True, verbose_name='وضعیت نمایش'),
        ),
    ]
