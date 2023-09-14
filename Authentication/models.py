from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from Authentication.manage import CustomUserManager
from django.utils import timezone
from django.db import models
import uuid
import os


# Create your models here.
def avatar_random_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('media/avatars/', filename)

def cover_image_random_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('media/cover_images/', filename)

class CusUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to=avatar_random_path, blank=True, null=True)
    cover_image = models.ImageField(upload_to=cover_image_random_path, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    short_bio = models.TextField(max_length=200, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=1, choices=(('0', 'Nam'), ('1', 'Nữ'), ('2', 'Khác')), default='2')
    address = models.CharField(max_length=30, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='user_groups', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permissions', related_query_name='user')
    is_active = models.BooleanField(default=True)
    is_status = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} - {self.id}'

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name

    def get_short_name(self):
        return self.first_name

    def get_gender(self):
        gender_dict = {'0': 'Nam', '1': 'Nữ', '2': 'Khác'}
        return gender_dict.get(self.gender, 'Khác')

    def get_default_cover_image(self):
        if not self.cover_image:
            self.cover_image = 'media/cover_images/defaults/default.png'

    def get_default_avatar(self):
        if not self.avatar:
            if self.gender == '0':
                self.avatar = 'media/avatars/defaults/male.png'
            elif self.gender == '1':
                self.avatar = 'media/avatars/defaults/female.png'
            else:
                self.avatar = 'media/avatars/defaults/default.png'

    def save(self, *args, **kwargs):
        if not self.artist:
            self.artist = self.get_full_name() if self.get_full_name() else self.username
        elif self.artist != self.get_full_name():
            self.artist = self.artist
        if not self.artist:
            self.artist = self.get_full_name() if self.get_full_name() else self.username

        if self.avatar:
            this = CusUser.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.name = ''
                this.save()
        elif not self.avatar:
            self.get_default_avatar()

        if self.cover_image:
            this = CusUser.objects.get(id=self.id)
            if this.cover_image != self.cover_image:
                this.cover_image.name = ''
                this.save()
        elif not self.cover_image:
            self.get_default_cover_image()

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'CusUser'
        verbose_name = 'CusUser'
        verbose_name_plural = 'CusUsers'
        ordering = ['id']
