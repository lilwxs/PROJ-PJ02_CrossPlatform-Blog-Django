from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from Authentication.models import CusUser
from pydub import AudioSegment
import uuid
import os

def blog_random_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('media/blogs/', filename)


def podcast_random_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('media/podcasts/', filename)


def audio_random_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('media/audios/', filename)

# |---------------------Create your models |Category| here.---------------------|
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    def slugify_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if self.name:
            if not self.slug or self.name != self.slugify_slug():
                self.slug = self.slugify_slug()
                if Category.objects.filter(slug=self.slug).exists():
                    counter = 1
                    while Category.objects.filter(slug=self.slug).exists():
                        self.slug = f"{self.slugify_slug()}_{counter}"
                        counter += 1
        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        ordering = ['-id']

# |---------------------Create your models |Blog| here.---------------------|
class Blog(models.Model):
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=blog_random_path, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    likes = models.ManyToManyField(CusUser, related_name='blog_likes', blank=True)
    dislikes = models.ManyToManyField(CusUser, related_name='blog_dislikes', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} - {self.user.username}'

    def get_absolute_url(self):
        return f'/blog/{self.slug}'

    def slugify_slug(self):
        return slugify(self.title)

    def save(self, *args, **kwargs):
        if self.title:
            if not self.slug or self.title != self.slugify_slug():
                self.slug = self.slugify_slug()
                if Blog.objects.filter(slug=self.slug).exists():
                    counter = 1
                    while Blog.objects.filter(slug=self.slug).exists():
                        self.slug = f"{self.slugify_slug()}&{counter}"
                        counter += 1
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Blog'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-created_at']


# |-----------------------Create your models |Playlist| here.-----------------------|
class Podcast(models.Model):
    TYPE_CHOICES = [
        ('single', 'Single'),
        ('album', 'Album'),
        ('ep', 'EP'),
        ('mixtape', 'Mixtape'),
        ('soundtrack', 'Soundtrack'),
        ('remix', 'Remix'),
        ('live', 'Live'),
        ('acoustic', 'Acoustic'),
        ('compilation', 'Compilation'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE, related_name='podcasts')
    title = models.CharField(max_length=100)
    types = models.CharField(max_length=100, choices=TYPE_CHOICES, default='other')
    image = models.ImageField(upload_to=podcast_random_path, blank=True, null=True)
    audio = models.FileField(upload_to=audio_random_path)
    lyrics = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='podcasts', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} - {self.user.artist}'

    def get_absolute_url(self):
        return f'/playlist/{self.slug}'

    def get_type_display(self):
        return dict(self.TYPE_CHOICES)[self.types]

    def slugify_slug(self):
        return slugify(self.title)

    def get_default_image(self):
        if not self.image:
            self.image = 'media/podcasts/defaults/default.png'

    def save(self, *args, **kwargs):
        if self.title:
            if not self.slug or self.title != self.slugify_slug():
                self.slug = self.slugify_slug()
                if Podcast.objects.filter(slug=self.slug).exists():
                    counter = 1
                    while Podcast.objects.filter(slug=self.slug).exists():
                        self.slug = f"{self.slugify_slug()}-{counter}"
                        counter += 1

        # Xử lý trường hợp người dùng không gán giá trị cho trường image
        if self.image:
            # Người dùng gán giá trị cho trường image
            try:
                this = Podcast.objects.get(id=self.id)
                if this.image != self.image:
                    # Xóa image default trong database
                    this.image.name = ''
                    this.save()
            except:
                pass
        else:
            # Người dùng không gán giá trị cho trường image, sử dụng image default
            self.get_default_image()

        # Xử lý giảm dung lượng file audio
        if self.audio:
            # Giảm dung lượng file audio
            try:
                this = Podcast.objects.get(id=self.id)
                if this.audio != self.audio:
                    # Giảm dung lượng file audio
                    audio = AudioSegment.from_file(self.audio)
                    audio.export(self.audio, format="mp3", bitrate="64k")
            except:
                pass

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Podcast'
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'
        ordering = ['-created_at']

# Ghi chú:
# 'single': Đại diện cho bài hát đơn (single).
# 'album': Đại diện cho album.
# 'ep': Đại diện cho EP (Extended Play).
# 'mixtape': Đại diện cho mixtape.
# 'soundtrack': Đại diện cho soundtrack.
# 'remix': Đại diện cho bài hát remix.
# 'live': Đại diện cho album hoặc bài hát thu âm từ buổi biểu diễn trực tiếp.
# 'acoustic': Đại diện cho bài hát phiên bản acoustic.
# 'compilation': Đại diện cho compilation album.
# 'other': Đại diện cho các loại type khác không được liệt kê.
