from django.urls import path
from . import views

urlpatterns = [
    # |------------------------GENERAL-------------------------------|
    path("", views.CusHomeView, name="home"),
    path("about", views.CusAboutView, name="about"),
    path("profile/<str:username>", views.CusProfileView, name="profile"),

    # |------------------------PROFILE------------------------|
    # path("profile/<str:username>/edit", views.CusProfileEditView, name="profile-edit"),
    path("profile/<str:username>/edit", views.UpdateAvatarFeature, name="avatar_edit"),
    path("profile/<str:username>/edit", views.UpdateCoverImageFeature, name="cover_image_edit"),

    # |------------------------BLOG---------------------------|
    path("newspaper-news", views.CusBlogView, name="blog"),
    path("news-detail/<str:slug>", views.CusBlogDetailView, name="blog-detail"),
    path('tao-bai-viet-moi/', views.CreateBlogFeature, name='blog_create'),
    path('chinh-sua-bai-viet/<str:slug>', views.UpdateBlogFeature, name='blog-update'),
    path('xoa-bai-viet/<str:slug>', views.DeleteBlogFeature, name='blog-delete'),

    # |------------------------PODCAST--------------------------|
    path("podcast", views.CusPodcastView, name="podcast"),
    path("podcast-detail/<str:slug>", views.CusPodcastDetailView, name="podcast-detail"),
    path('tao-ban-nhac-moi/', views.CreatePodcastFeature, name='podcast_create'),
    path('xoa-podcast/<str:slug>', views.DeletePodcastFeature, name='podcast_delete'),

    # |------------------------COMMENT--------------------------|
    path('tao-binh-luan/<str:slug>', views.CreateCommentFeature, name='comment-create'),
    path('update/<str:slug>', views.UpdateCommentFeature, name='comment-update'),
    path('delete/<int:pk>', views.DeleteCommentFeature, name='comment-delete'),

    # |------------------------REPLY--------------------------|
    path('tao-tra-loi/<int:pk>', views.CreateReplyFeature, name='reply-create'),
    # path('update/<str:slug>', views.UpdateReplyFeature, name='reply-update'),
    path('delete/<int:pk>', views.DeleteReplyFeature, name='reply-delete'),

    # |------------------------REACTION--------------------------|
    path('reaction_feature/<str:slug>', views.ReactionFeature, name='reaction'),

    # |------------------------SEARCH--------------------------|
    path('search', views.SearchFeature, name='search'),
]
