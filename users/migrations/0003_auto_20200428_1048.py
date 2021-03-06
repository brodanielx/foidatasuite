# Generated by Django 3.0.5 on 2020-04-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200422_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Tampa, FL', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='nation_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='rank',
            field=models.CharField(default='Officer', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='receive_emails',
            field=models.BooleanField(default=False),
        ),
    ]
