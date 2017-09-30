# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0042_auto_20160602_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcertOrder',
            fields=[
                ('ticketorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='merchandise.TicketOrder')),
                ('shipping_address', models.CharField(blank=True, max_length=40, verbose_name='\u6536\u7968\u5730\u5740')),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concertorders', to='merchandise.UserMerchandise')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='merchandise.ConcertTicket')),
            ],
            options={
                'verbose_name': '\u6f14\u5531\u4f1a\u7968\u8ba2\u5355',
                'verbose_name_plural': '\u6f14\u5531\u4f1a\u7968\u8ba2\u5355',
            },
            bases=('merchandise.ticketorder',),
        ),
    ]
