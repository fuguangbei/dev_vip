#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import vip.utils as utils


def post_banner_upload_path(instance, filename):
	ext = utils.get_file_extension(filename)
	file_path = "explore/posts/{id}/banner.{ext}"
	return file_path.format(id=instance.pk, ext=ext)


def post_video_upload_path(instance, filename):
	ext = utils.get_file_extension(filename)
	file_path = "explore/posts/{id}/video.{ext}"
	return file_path.format(id=instance.pk, ext=ext)


@python_2_unicode_compatible
class Post(models.Model):
	class Meta:
		verbose_name = '发现'
		verbose_name_plural = '发现'
	title = models.CharField(max_length=30, verbose_name='标题')
	banner = models.ImageField(
		upload_to=post_banner_upload_path,
		verbose_name="顶部封面图",
	)
	video = models.TextField(
		verbose_name='视频链接',
		blank=True,
		default=''
	)
	caption_title = models.CharField(
		max_length=10,
		verbose_name='推荐标题描述'
	)
	caption_description = models.CharField(
		max_length=30,
		verbose_name='推荐内容描述'
	)
	date = models.DateTimeField(verbose_name='发布日期', auto_now_add=True)
	content = RichTextUploadingField(verbose_name='正文')

	def get_cover(self):
		return self.get_video_cover() if self.video else self.get_image_cover()

	def get_image_cover(self):
		return self.banner.url if self.banner else ''

	def get_video_cover(self):
		return self.video

	def has_video(self):
		if not self.video or len(self.video) == 0:
			return False
		return True

	def save(self, *args, **kwargs):
		if self.pk is None:
			saved_image = self.banner
			self.banner = None
			super(Post, self).save(*args, **kwargs)
			self.banner = saved_image
		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	def extract_content(self):
		from bs4 import BeautifulSoup as bs
		a = bs(self.content, 'html.parser')
		return a.get_text()

	def to_json(self):
		this = {
			'id': self.pk,
			'cover': self.get_image_cover(),
			'video': self.get_video_cover(),
			'title': self.title,
			'content': self.extract_content(),
			# 'date': self.date.date(),
			'raw_content': self.content,
			'caption_title': self.caption_title,
			'caption_description': self.caption_description,
			'has_video': self.has_video(),
		}
		return this


@python_2_unicode_compatible
class UserExplore(models.Model):
	class Meta:
		verbose_name = '用户发现'
		verbose_name_plural = '用户发现'

	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
	)
	explore_likes = models.ManyToManyField(
		Post,
		verbose_name='已收藏发现',
		blank=True
	)

	def toggle_like_explore(self, post):
		if post in self.explore_likes.all():
			self.explore_likes.remove(post)
			return False
		else:
			self.explore_likes.add(post)
			return True

	def __str__(self):
		return self.user.username

@python_2_unicode_compatible
class ExploreComments(models.Model):
	class Meta:
		verbose_name = '发现评论'
		verbose_name_plural = '发现评论'
	publish_time = models.DateTimeField(auto_now_add=True)
	content = models.CharField(max_length=140, verbose_name='评论')
	corresponding_post = models.ForeignKey(
		Post,
		related_name='explore_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
		)
	corresponding_user = models.ForeignKey(
		User,
		related_name='user_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)

	def __str__(self):
		#return str(self.pk)
		return self.content

	def to_json(self):
		user_info = {
			'name': self.corresponding_user.profile.get_nickname(),
			'avatar': self.corresponding_user.profile.get_avatar()
		}
		this = {
			'id': self.pk,
			'user': user_info,
			# 'date': self.publish_time,
			'text': self.content
		}
		return this

@python_2_unicode_compatible
class Highlight(models.Model):
	cover_image = models.ImageField(
		verbose_name='封面图',
		upload_to=utils.get_explore_highlight_upload_path,
		blank=True,
		default=""
	)
	link = models.ForeignKey(
		Post,
		on_delete=models.CASCADE
	)
	display = models.BooleanField(
		verbose_name='是否显示',
		default=False
	)

	def save(self, *args, **kwargs):
		if self.pk is None:
			saved_image = self.cover_image
			self.cover_image = None
			super(Highlight, self).save(*args, **kwargs)
			self.cover_image = saved_image
		super(Highlight, self).save(*args, **kwargs)

	def __str__(self):
		return self.link.title

	def to_json(self):
		if self.cover_image:
			image_url = self.cover_image.url
		elif self.link.banner:
			image_url = self.link.banner.url
		else:
			image_url = ""
		this = {
			"cover": image_url,
			"link": self.link.pk,
			'has_video': self.link.has_video()
		}
		return this