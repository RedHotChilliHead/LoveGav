from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from blogapp.forms import CommentForm
from blogapp.models import Post, Comment
from profileapp.models import Profile


class UserPublicDetaislView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра публичного профиля владельца
    """

    model = Profile
    template_name = 'blogapp/public_user_profile.html'
    context_object_name = 'profile'  # Имя объекта профиля в контексте шаблона

    def get_object(self, queryset=None):
        return get_object_or_404(Profile.objects.select_related('user'), user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        # Предварительная загрузка постов пользователя
        posts = Post.objects.filter(author=profile.user).prefetch_related('comment_set')
        context['posts'] = posts
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Представление для создания поста
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


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования поста
    """

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_staff or self.request.user.pk == post.author.id:
            return True

    model = Post
    fields = "description", "photo"
    template_name = 'blogapp/post_update.html'

    def get_success_url(self):
        return reverse_lazy("blogapp:detail-post", kwargs={'pk': self.object.pk, 'username': self.object.author.username})


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления поста
    """

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_staff or self.request.user.pk == post.author.id:
            return True

    model = Post
    template_name = "blogapp/post_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("blogapp:public-user-details", kwargs={'username': self.object.author.username})


class PostDetaislView(LoginRequiredMixin, View):
    """
    Представление для просмотра поста и комментариев к ним
    """

    def get(self, request, *args, **kwargs):

        post = get_object_or_404(Post.objects.select_related('author'), pk=self.kwargs['pk'])
        form = CommentForm()
        context = {
            "post": post,
            "form": form,
            'permission': self.request.user.is_staff or self.request.user.pk == post.author.id,
        }
        return render(request, 'blogapp/post_details.html', context=context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.select_related('author'), pk=self.kwargs['pk'])
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blogapp:public-user-details', username=post.author.username)
        else:
            context = {
                "post": post,
                "form": form,
                'permission': self.request.user.is_staff or self.request.user.pk == post.author.id
            }
            return render(request, 'blogapp/post_details.html', context=context)


class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления комменатария к посту
    """

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        if self.request.user.is_staff or self.request.user.pk == comment.author.id:
            return True

    model = Comment
    template_name = "blogapp/comment_confirm_delete.html"

    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        post = get_object_or_404(Post, pk=comment.post.pk)
        return reverse_lazy("blogapp:detail-post", kwargs={'pk': post.pk, 'username': post.author.username})


class PostListView(ListView):
    """
    Представление для отображения ленты постов
    """
    template_name = 'blogapp/post_list.html'
    paginate = 30
    model = Post

    # queryset = (
    #     Post.objects
    #     .prefetch_related("author").select_related("author__profile").prefetch_related("comment_set")
    # )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['permission'] = True
        return context


