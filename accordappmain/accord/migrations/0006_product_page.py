# Generated by Django 3.2.8 on 2022-04-18 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accord', '0005_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accord.pages'),
        ),
    ]
