# Generated by Django 5.1.1 on 2024-10-27 10:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_adoptiontransaction_transaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adoptiontransaction',
            name='adoption_date',
        ),
        migrations.AddField(
            model_name='adoptiontransaction',
            name='transaction_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
