from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, PostForm
from .models import Post, Comment
import requests
from bs4 import BeautifulSoup


def index(request):
    page = 1
    all_news = []
    if len(Post.objects.all()) < 1000:
        for i in range(page):
            if i == 1:
                html_doc = requests.get(f'https://news.ycombinator.com/newest?next=30056583&n={i}')
            else:
                html_doc = requests.get(f'https://news.ycombinator.com/newest?next=30056583&n={i * 30}')
            soup = BeautifulSoup(html_doc.text)
            items = soup.find_all('a', class_='titlelink')
            comments = soup.find_all('td', class_='subtext')
            pus = []
            for j, o in zip(items, comments):
                all_news.append(j)
                adder = Post.objects.create(title=j.text, url=j['href'])
                adder.save()
                # return HttpResponse(adder.pk)
                for das in o:
                    if '<a href="item?id=' in str(das):
                        comment = das.a['href']
                        com_site = requests.get('https://news.ycombinator.com/' + str(comment))
                        comm = BeautifulSoup(com_site.text)
                        comms = comm.find_all('table', class_='comment-tree')
                        for chto in comms:
                            dastaq = Comment.objects.create(text=chto, from_post=adder.pk)
                            dastaq.save()
                        pus.append(comment)
                        break
            return HttpResponse(pus)

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # return HttpResponse(post_list)
    return render(request, 'List/index.html', {'page_obj': page_obj})

@login_required()
def author(request, username):
    author_list = Post.objects.filter(author__username=username)
    return render(request, 'List/author.html', {'author_list': author_list, 'username': username})


@login_required()
def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment = Comment.object.filter(from_post=pk)
    return render(request, 'List/detail.html', {'post': post, 'comment': comment})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, аккаунт успешно зарегестрирован!')
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'List/register.html', {'form': form})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'List/post_edit.html', {'form': form})


@login_required()
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')


@login_required()
def post_delete_all(request):
    post = Post.objects.all()
    post.delete()
    return redirect('/')


@login_required()
def post_done(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.make_it_done()
    post.save()
    return redirect('/')


@login_required()
def post_not_done(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.make_it_undone()
    post.save()
    return redirect('/')
