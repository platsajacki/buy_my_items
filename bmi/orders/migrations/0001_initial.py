# Generated by Django 5.0.2 on 2024-02-28 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('items', models.ManyToManyField(related_name='orders', to='items.item', verbose_name='items')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='id')),
                ('orders', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discounts', to='orders.order', verbose_name='orders')),
            ],
            options={
                'verbose_name': 'discount',
                'verbose_name_plural': 'discounts',
                'ordering': ('modified',),
            },
        ),
    ]
