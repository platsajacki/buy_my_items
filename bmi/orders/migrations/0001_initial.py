# Generated by Django 5.0.2 on 2024-02-27 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('coupon_stripe_id', models.CharField(max_length=255, unique=True, verbose_name='coupon stripe id')),
            ],
            options={
                'verbose_name': 'discount',
                'verbose_name_plural': 'discounts',
                'ordering': ('modified',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('discounts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.discount', verbose_name='discounts')),
                ('items', models.ManyToManyField(related_name='orders', to='items.item', verbose_name='items')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('created',),
            },
        ),
    ]
