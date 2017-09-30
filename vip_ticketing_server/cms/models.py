# coding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

# Create your models here.
@python_2_unicode_compatible
class Sensitive(models.Model):
    class Meta:
        verbose_name = '敏感词'
        verbose_name_plural = '敏感词'

    words = models.CharField(max_length=7, default='', blank=True)
    time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    added = models.ForeignKey(
        User,
        related_name='added_user',
        verbose_name='添加人',
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            # saved_image = self.banner
            # self.banner = None
            super(Sensitive, self).save(*args, **kwargs)
            # self.banner = saved_image
        super(Sensitive, self).save(*args, **kwargs)

    def __str__(self):
        return self.words
    # def __unicode__(self):
    #     return unicode(self.words)

@python_2_unicode_compatible
class Feedback(models.Model):
    class Meta:
        verbose_name = '意见反馈'
        verbose_name_plural = '意见反馈'

    content = models.CharField(max_length=140, default='', blank=True)
    submit_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    solved_time = models.DateTimeField(verbose_name='解决时间', blank=True, null=True)
    is_solved = models.BooleanField(default=False, verbose_name='是否已处理')

    def __str__(self):
        return str(self.pk)