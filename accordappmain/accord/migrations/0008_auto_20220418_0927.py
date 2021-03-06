# Generated by Django 3.2.8 on 2022-04-18 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accord', '0007_remove_product_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_contactnumber',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
