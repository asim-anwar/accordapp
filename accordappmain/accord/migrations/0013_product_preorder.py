# Generated by Django 3.2.8 on 2022-04-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accord', '0012_auto_20220418_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='preorder',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
