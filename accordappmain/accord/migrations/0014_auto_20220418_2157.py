# Generated by Django 3.2.8 on 2022-04-18 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accord', '0013_product_preorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='created_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
