# Generated by Django 3.2.8 on 2022-05-20 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accord', '0021_auto_20220520_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_by_order', to=settings.AUTH_USER_MODEL),
        ),
    ]
