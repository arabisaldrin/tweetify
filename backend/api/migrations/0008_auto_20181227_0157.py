# Generated by Django 2.1.4 on 2018-12-27 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20181226_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
