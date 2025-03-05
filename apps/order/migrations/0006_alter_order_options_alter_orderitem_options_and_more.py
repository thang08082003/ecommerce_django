# Generated by Django 5.1.5 on 2025-03-03 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobiles', '0002_alter_mobile_options_remove_mobile_color_and_more'),
        ('order', '0005_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-order_date'], 'verbose_name': 'Đơn hàng', 'verbose_name_plural': 'Đơn hàng'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Chi tiết đơn hàng', 'verbose_name_plural': 'Chi tiết đơn hàng'},
        ),
        migrations.AddField(
            model_name='orderitem',
            name='mobile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobiles.mobile'),
        ),
    ]
