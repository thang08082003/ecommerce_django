# Generated by Django 5.1.5 on 2025-03-03 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('cart', '0001_initial'),
        ('shoes', '0002_alter_shoes_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='shoes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shoes.shoes'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book'),
        ),
    ]
