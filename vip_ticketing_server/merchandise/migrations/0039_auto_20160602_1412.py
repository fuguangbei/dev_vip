# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 06:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0038_auto_20160602_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=11, verbose_name='\u8ba2\u5355\u53f7')),
                ('count', models.IntegerField(verbose_name='\u6570\u91cf')),
                ('order_date', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': '\u5546\u54c1\u8ba2\u5355',
                'verbose_name_plural': '\u5546\u54c1\u8ba2\u5355',
            },
        ),
        migrations.CreateModel(
            name='DisneyOrder',
            fields=[
                ('ticketorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='merchandise.TicketOrder')),
                ('identification', models.CharField(max_length=18, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('pickup', models.BooleanField(default=False, verbose_name='\u662f\u5426\u63a5\u9001')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='merchandise.DisneyTicket')),
            ],
            options={
                'verbose_name': '\u8fea\u58eb\u5c3c\u95e8\u7968\u8ba2\u5355',
                'verbose_name_plural': '\u8fea\u58eb\u5c3c\u95e8\u7968\u8ba2\u5355',
            },
            bases=('merchandise.ticketorder',),
        ),
        migrations.AddField(
            model_name='ticketorder',
            name='purchaser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticketorders', to='merchandise.UserMerchandise'),
        ),
    ]
