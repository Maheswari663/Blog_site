from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post
from .forms import PostForm
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q 
from datetime import datetime





def home(request):
    query = request.GET.get('q')
    print("QUERY RECEIVED = ", query)
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')

    else:   
        posts_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts_list,3)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)


    return render(request, 'home.html', 
                  {'posts': posts,
                   'query':query,
                   'now': datetime.now()
                   })

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'detail.html', {'post': post,'now': datetime.now()})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # slug automatic generate
            post.slug = slugify(post.title)
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form, 'now': datetime.now()})


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)  # optional: update slug
            post.save()
            return redirect('detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post, 'now': datetime.now()})


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'home/delete_post.html', {'post': post, 'now': datetime.now()})



