# Generated by Django 3.1 on 2020-08-20 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200820_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='bids',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='comments',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction'),
        ),
        migrations.AddField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction'),
        ),
    ]
