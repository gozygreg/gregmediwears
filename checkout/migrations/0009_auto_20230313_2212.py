# Generated by Django 3.2 on 2023-03-13 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='original_bag',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_pid',
            field=models.CharField(default='', max_length=254),
        ),
    ]
