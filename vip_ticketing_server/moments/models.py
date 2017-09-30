# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import vip.utils as utils
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
def post_image_upload_path(instance, filename):
	ext = utils.get_file_extension(filename)
	file_path = "moments/posts/{id}/image.{ext}"
	return file_path.format(id=instance.pk, ext=ext)


@python_2_unicode_compatible
class Post(models.Model):
	class Meta:
		verbose_name = '圈子'
		verbose_name_plural = '圈子'

	text = models.CharField(max_length=140, verbose_name='正文')
	banner = models.ImageField(
		upload_to=post_image_upload_path,
		verbose_name="圈子封面图",
		blank=True,
		null=True
	)
	date = models.DateTimeField(verbose_name='发布日期', auto_now_add=True)
	publisher = models.ForeignKey(
		User,
		related_name='published_moments',
		on_delete=models.CASCADE,
		verbose_name='发布人'
	)
	author = models.ForeignKey(
		User,
		related_name='composed_moments',
		on_delete=models.CASCADE,
		verbose_name='作者'
	)
	forward_notes = models.CharField(
		max_length=140,
		verbose_name='转发文字',
		blank=True,
		default=""
	)
	display = models.BooleanField(
		verbose_name='是否显示',
		default=False
	)

	def save(self, *args, **kwargs):
		if self.pk is None:
			saved_image = self.banner
			self.banner = None
			super(Post, self).save(*args, **kwargs)
			self.banner = saved_image
		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.text

	def to_json(self):
		publisher_info = {
			'userid':self.publisher.pk,
			'name': self.publisher.profile.get_nickname(),
			'avatar': self.publisher.profile.get_avatar()
		}
		this = {
			'id': self.pk,
			'text': self.text,
			'image': self.banner.url if self.banner else '',
			'publisher': publisher_info,
			'verified': self.display,
			'publish_time': self.date
		}
		if self.publisher != self.author:
			this['author'] = self.author.profile.get_nickname()
			this['caption'] = self.forward_notes
		return this


@python_2_unicode_compatible
class UserMoments(models.Model):
	class Meta:
		verbose_name = '用户圈子'
		verbose_name_plural = '用户圈子'

	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE
	)

	moments_likes = models.ManyToManyField(
		Post,
		verbose_name='已点赞圈子',
		blank=True
	)

	def toggle_like_moments(self, post):
		if post in self.moments_likes.all():
			self.moments_likes.remove(post)
			self.save()
			return "取消点赞圈子: {0}".format(post.id)
		else:
			self.moments_likes.add(post)
			self.save()
			return "点赞圈子: {0}".format(post.id)

	def __str__(self):
		return self.user.username


@python_2_unicode_compatible
class MomentsComments(models.Model):
	class Meta:
		verbose_name = '圈子评论'
		verbose_name_plural = '圈子评论'

	publish_time = models.DateTimeField(auto_now_add=True)
	content = models.CharField(max_length=140, verbose_name='评论')
	corresponding_post = models.ForeignKey(
		Post,
		related_name='moments_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	corresponding_user = models.ForeignKey(
		User,
		related_name='moments_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)

	def __str__(self):
		return self.content

	def to_json(self):
		user_info = {
			'userid': self.corresponding_user.pk,
			'name': self.corresponding_user.profile.get_nickname(),
			'avatar': self.corresponding_user.profile.get_avatar()
		}
		this = {
			'id': self.pk,
			'user': user_info,
			'text': self.content
		}
		return this
