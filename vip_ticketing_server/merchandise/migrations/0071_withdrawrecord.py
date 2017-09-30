# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 06:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchandise', '0070_ticket_bonus_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdraw_datetime', models.DateTimeField(verbose_name='\u63d0\u73b0\u65f6\u95f4')),
                ('status', models.BooleanField(default=False, verbose_name='\u5df2\u63d0\u73b0')),
                ('amount', models.FloatField(verbose_name='\u63d0\u73b0\u91d1\u989d')),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawables', to=settings.AUTH_USER_MODEL, verbose_name='\u53d7\u76ca\u4eba')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawables', to='merchandise.TicketOrder', verbose_name='\u8ba2\u5355')),
            ],
        ),
    ]
