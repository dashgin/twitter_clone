# Generated by Django 3.1.12 on 2021-07-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20210704_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='is_retweet',
            field=models.BooleanField(default=False),
        ),
    ]