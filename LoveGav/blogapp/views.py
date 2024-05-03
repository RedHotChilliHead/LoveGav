from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView

from blogapp.forms import CommentForm
from blogapp.models import Post, Comment
from profileapp.models import Profile


class UserPublicDetaislView(LoginRequiredMixin, DetailView):
    """
    Просмотр публичного профиля владельца
    """

    model = Profile
    template_name = 'blogapp/public_user_profile.html'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs['username'])
        profile = get_object_or_404(Profile, user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        context['posts'] = Post.objects.filter(author=self.object.user)
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Создать пост
    """
    model = Post
    fields = "description", "photo"
    template_name = 'blogapp/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy("blogapp:public-user-details", kwargs={'username': self.request.user.username})

class PostDetaislView(LoginRequiredMixin, View):
    """
    Посмотреть пост и комментарии
    """

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form = CommentForm()
        comments = Comment.objects.filter(post=post)
        context = {
            "post": post,
            "form": form,
            "comments": comments,
            'permission': self.request.user.is_staff or self.request.user.pk == post.author.id
        }
        return render(request, 'blogapp/post_details.html', context=context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blogapp:public-user-details', username=post.author.username)
        else:
            comments = Comment.objects.filter(post=post)
            context = {
                "post": post,
                "form": form,
                "comments": comments,
                'permission': self.request.user.is_staff or self.request.user.pk == post.author.id
            }
            return render(request, 'blogapp/post_details.html', context=context)


