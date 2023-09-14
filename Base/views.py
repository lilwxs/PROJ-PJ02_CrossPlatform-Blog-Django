from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from Authentication.models import CusUser
from Base.multiplatform_models import Blog, Podcast, Category
from Base.models import Viewer, Comment, Reply
from random import shuffle


# |----------HOME--------------HOME-----------------------HOME--------|
def CusHomeView(request):
    users = CusUser.objects.all().order_by('-date_joined')
    categories = Category.objects.all()
    blogs = Blog.objects.all().order_by('-created_at')
    podcasts = Podcast.objects.all().order_by('-created_at')
    outstanding_blogs = blogs[:5]
    outstanding_podcasts = podcasts[:5]
    outstanding_blogs = sorted(outstanding_blogs, key=lambda x: x.viewers.count(), reverse=True)
    # outstanding_podcasts = sorted(outstanding_podcasts, key=lambda x: x.viewers.count(), reverse=True)
    # Phân loại theo category
    category = request.GET.get('category')
    if category:
        blogs = Blog.objects.filter(category__name=category).order_by('-created_at')
        podcasts = Podcast.objects.filter(category__name=category).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
        podcasts = Podcast.objects.all().order_by('-created_at')

    items = list(blogs) + list(podcasts)
    shuffle(list(users))
    shuffle(items)

    context = {
        'items': items,
        'users': users,
        'categories': categories,
        'outstanding_blogs': outstanding_blogs,
        'outstanding_podcasts': outstanding_podcasts,
    }
    return render(request, "pages/home.html", context)


# |-----ABOUT-------------------ABOUT------------ABOUT-------------------|
def CusAboutView(request):
    return render(request, "pages/about.html")


# |-----------PROFILE-------------PROFILE---------------------------PROFILE--|
def CusProfileView(request, username):
    user = CusUser.objects.get(username=username)
    blogs = Blog.objects.filter(user=user)
    podcasts = Podcast.objects.filter(user=user)
    length_blogs = blogs[:9]
    context = {'user': user, 'blogs': blogs, 'podcasts': podcasts, 'length_blogs': length_blogs}
    return render(request, "common/_profile/profile.html", context)


# |----------BLOG----------------BLOG------------------------BLOG----|
def CusBlogView(request):
    blogs = list(Blog.objects.all().order_by('-created_at'))
    shuffle(blogs)

    context = {'blogs': blogs}
    return render(request, "common/_blog/blog.html", context)


# |----------BLOG DETAIL----------------BLOG DETAIL------------------------BLOG DETAIL----|
def CusBlogDetailView(request, slug):
    blog = Blog.objects.all().order_by('-created_at')
    blog_list = list(blog)
    shuffle(blog_list)
    categories = Category.objects.all().order_by('name')
    # Tăng viewer
    blogs = Blog.objects.filter(slug=slug).first()
    if request.user.is_authenticated:
        user = CusUser.objects.get(username=request.user.username)
        Viewer.objects.get_or_create(blog=blogs, user=user)

    context = {'blogs': blogs, 'blog_list': blog_list, 'categories': categories}
    return render(request, "common/_blog/blog_detail.html", context)


# |---PODCAST---------------------PODCAST------------PODCAST--------------|
def CusPodcastView(request):
    podcasts = list(Podcast.objects.all().order_by('-created_at'))
    shuffle(podcasts)

    context = {'podcasts': podcasts}
    return render(request, "common/_podcast/podcast.html", context)


# |---PODCAST DETAIL---------------------PODCAST DETAIL------------PODCAST DETAIL--------------|
def CusPodcastDetailView(request, slug):
    podcast = Podcast.objects.all().order_by('-created_at')
    podcast_list = list(podcast)
    shuffle(podcast_list)
    podcasts = Podcast.objects.filter(slug=slug).first()

    context = {'podcasts': podcasts, 'podcast_list': podcast_list}
    return render(request, "common/_podcast/podcast_detail.html", context)


# |---CREATE_BLOG---------------------CREATE_BLOG------------CREATE_BLOG--------------|
def CreateBlogFeature(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        user = CusUser.objects.get(username=request.user.username)
        title = request.POST.get('title')
        category_name = request.POST.get('category')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if title != '' and category_name != '' and content != '' and image != '':
            category = Category.objects.get(name=category_name)
            Blog.objects.create(user=user, title=title, category=category, content=content, image=image)
            return redirect(reverse('blog'))
    context = {'categories': categories}
    return render(request, "features/_blog/_blog_create.html", context)


# |---UPDATE_BLOG---------------------UPDATE_BLOG------------UPDATE_BLOG--------------|
def UpdateBlogFeature(request, slug):
    if request.method == 'POST':
        blog = Blog.objects.get(slug=slug)
        title = request.POST.get('title')
        category_name = request.POST.get('category')
        content = request.POST.get('content')
        if title != '' and category_name != '' and content != '':
            category = Category.objects.get(name=category_name)
            blog.title = title
            blog.category = category
            blog.content = content
            blog.save()
            return redirect(reverse('blog-detail', kwargs={'slug': blog.slug}))
    return redirect(request.META.get('HTTP_REFERER'))


# |---DELETE_BLOG---------------------DELETE_BLOG------------DELETE_BLOG--------------|
def DeleteBlogFeature(request, slug):
    if request.method == 'POST':
        blog = Blog.objects.get(slug=slug)
        blog.delete()
    return redirect(reverse('blog'))


# |---CREATE_PODCAST---------------------CREATE_PODCAST------------CREATE_PODCAST--------------|
def CreatePodcastFeature(request):
    if request.method == 'POST':
        user = CusUser.objects.get(username=request.user.username)
        title = request.POST.get('title')
        lyrics = request.POST.get('lyrics')
        audio = request.FILES.get('audio')
        image = request.FILES.get('image')
        if title != '' and lyrics != '' and audio != '' and image != '':
            Podcast.objects.create(user=user, title=title, lyrics=lyrics, audio=audio, image=image)
            return redirect(reverse('podcast'))
    return render(request, "features/_podcast/_podcast_create.html")


# |---DELETE_PODCAST---------------------DELETE_PODCAST------------DELETE_PODCAST--------------|
def DeletePodcastFeature(request, slug):
    if request.method == 'POST':
        podcast = Podcast.objects.get(slug=slug)
        podcast.delete()
    return redirect(reverse('podcast'))


# |---COMMENT---------------------COMMENT------------COMMENT--------------|
def CreateCommentFeature(request, slug):
    if request.method == 'POST':
        user = CusUser.objects.get(username=request.user.username)
        blog = Blog.objects.get(slug=slug)
        content = request.POST.get('content')
        if content != '':
            blog.comments.create(user=user, content=content)
    return redirect(request.META.get('HTTP_REFERER'))


# |---UPDATE---------------------UPDATE------------UPDATE--------------|
def UpdateCommentFeature(request, slug):
    pass


# |---DELETE---------------------DELETE------------DELETE--------------|
def DeleteCommentFeature(request, pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=pk)
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))


# |---REPLY---------------------REPLY------------REPLY--------------|
def CreateReplyFeature(request, pk):
    if request.method == 'POST':
        user = CusUser.objects.get(username=request.user.username)
        comment = Comment.objects.get(pk=pk)
        content = request.POST.get('content')
        if content != '':
            comment.replies.create(user=user, content=content)
    return redirect(request.META.get('HTTP_REFERER'))


# |---DELETE---------------------DELETE------------DELETE--------------|
def DeleteReplyFeature(request, pk):
    if request.method == 'POST':
        reply = Reply.objects.get(pk=pk)
        reply.delete()
    return redirect(request.META.get('HTTP_REFERER'))


# |---SEARCH---------------------SEARCH------------SEARCH--------------|
def SearchFeature(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
            podcasts = Podcast.objects.filter(Q(title__icontains=keyword) | Q(lyrics__icontains=keyword))
            items = list(blogs) + list(podcasts)
            context = {'items': items}
            return render(request, "pages/search.html", context)
    return redirect(request.META.get('HTTP_REFERER'))


# |-------Reaction-----------------Reaction-----------------Reaction-----------------|
def ReactionFeature(request, slug):
    if request.method == 'POST':
        blog = Blog.objects.get(slug=slug)
        user = CusUser.objects.get(username=request.user.username)
        reaction = request.POST.get('reaction')

        if reaction == 'like':
            if user in blog.likes.all():
                blog.likes.remove(user)
            elif user in blog.dislikes.all():
                blog.dislikes.remove(user)
                blog.likes.add(user)
            else:
                blog.likes.add(user)
        elif reaction == 'dislike':
            if user in blog.dislikes.all():
                blog.dislikes.remove(user)
            elif user in blog.likes.all():
                blog.likes.remove(user)
                blog.dislikes.add(user)
            else:
                blog.dislikes.add(user)

    return redirect(request.META.get('HTTP_REFERER'))


# |-------UPDATE COVER IMGAE - PROFILE IMAGE-----------------UPDATE COVER IMGAE - PROFILE IMAGE-----------------|
def UpdateCoverImageFeature(request, username):
    if request.method == 'POST':
        user = CusUser.objects.get(username=username)
        cover_image = request.FILES.get('cover_image')
        if cover_image != '':
            user.cover_image = cover_image
            user.save()
    return redirect(request.META.get('HTTP_REFERER'))

# |-----------UPDATE AVATAR PROFILE-----------------UPDATE AVATAR PROFILE-----------------|
def UpdateAvatarFeature(request, username):
    if request.method == 'POST':
        user = CusUser.objects.get(username=username)
        avatar = request.FILES.get('avatar')
        if avatar != '':
            user.avatar = avatar
            user.save()
    return redirect(request.META.get('HTTP_REFERER'))
