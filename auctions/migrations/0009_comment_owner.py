# Generated by Django 3.1 on 2020-08-27 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auction_watchlisted'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
