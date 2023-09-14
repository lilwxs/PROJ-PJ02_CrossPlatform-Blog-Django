from django.contrib import admin
from Base.multiplatform_models import Blog, Podcast, Category
from Base.models import Viewer, Comment, Reply

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1

class ViewerInline(admin.TabularInline):
    model = Viewer
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user')
    ordering = ('-created_at',)
    inlines = [ViewerInline, CommentInline]

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user')
    ordering = ('-created_at',)

class ViewerAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    list_filter = ('blog', 'user')
    search_fields = ('blog', 'user')
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    list_filter = ('blog', 'user')
    search_fields = ('blog', 'user')
    ordering = ('-created_at',)
    inlines = [ReplyInline]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Viewer, ViewerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)