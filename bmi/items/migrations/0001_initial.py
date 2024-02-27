# Generated by Django 5.0.2 on 2024-02-27 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('tax_stripe_id', models.CharField(max_length=255, unique=True, verbose_name='tax stripe id')),
            ],
            options={
                'verbose_name': 'tax',
                'verbose_name_plural': 'taxes',
                'ordering': ('modified',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(max_length=512, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='price')),
                ('currency', models.CharField(choices=[('usd', 'dollar'), ('eur', 'euro')], verbose_name='currency')),
                ('taxes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='items.tax', verbose_name='taxes')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ('name',),
            },
        ),
    ]
