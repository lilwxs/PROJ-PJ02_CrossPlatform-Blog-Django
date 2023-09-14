from django.db import models
from django.utils import timezone
from Authentication.models import CusUser
from Base.multiplatform_models import Blog

# Create your models here.
class Viewer(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='viewers')
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"

    class Meta:
        db_table = 'Viewer'
        unique_together = ('blog', 'user')
        verbose_name = 'Viewer'
        verbose_name_plural = 'Viewers'
        ordering = ['-created_at']

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"

    class Meta:
        db_table = 'Comment'
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'
        ordering = ['-created_at']

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.comment.blog.title}"

    class Meta:
        db_table = 'Reply'
        verbose_name_plural = 'Replies'
        verbose_name = 'Reply'
        ordering = ['-created_at']

class Reaction(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(CusUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"

    class Meta:
        db_table = 'Reaction'
        unique_together = ('blog', 'user')
        verbose_name_plural = 'Reactions'
        verbose_name = 'Reaction'
        ordering = ['-created_at']