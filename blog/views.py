from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.urls import reverse
from .models import *
#from django.http import HttpResponse
from .utils import *
from .forms import TagForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

# POST
class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    modelForm = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostUpdate(LoginRequiredMixin, ObjectsUpdateMixin, View):
    model = Post
    modelForm = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin ,View):
    model = Post
    template = 'blog/post_delete_form.html'
    template_of_list = 'post_list_url'
    raise_exception = True


def post_list(request)->'html':
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query)| Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)

    page_number = request.GET.get('page', default=1)

    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''
    context = {'page_object': page,
               'is_paginated': is_paginated,
               'next_url':next_url,
               'prev_url':prev_url}

    return render(request,
                  'blog/index.html',
                  context=context)


# TAG
class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    modelForm = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagUpdate(LoginRequiredMixin, ObjectsUpdateMixin, View):
    model = Tag
    modelForm = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin ,View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    template_of_list = 'tags_list_url'
    raise_exception = True


def tags_list(request)->'html':
    tags = Tag.objects.all()
    return render(request,
                  'blog/tags_list.html',
                  context={'tags':tags})
