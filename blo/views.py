from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import  User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin,
                                        )


def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, 'blo/home.html', context)


# def blogLike(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post-id'))
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostListView(ListView):
    model = Post
    template_name = 'blo/home.html'  # <app>/<model>/_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #
    #     likes_gotten = get_object_or_404(Post, id= self.kwargs['pk'])
    #     liked = False
    #     if likes_gotten.likes.filter(id= self.request.user.id).exists():
    #         liked =True
    #         data['number_of_likes'] =likes_gotten.number_of_likes()
    #         data['post_is_liked'] = liked
    #         return data



class UserPostListView(ListView):
    model = Post
    template_name = 'blo/user_posts.html'  # <app>/<model>/_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username =self.kwargs.get('username'))
        return  Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #
    #     likes_gotten = get_object_or_404(Post, id= self.kwargs['pk'])
    #     liked = False
    #     if likes_gotten.likes.filter(id= self.request.user.id).exists():
    #         liked =True
    #         data['number_of_likes'] =likes_gotten.number_of_likes()
    #         data['post_is_liked'] = liked
    #         return data


class PostCreateView(LoginRequiredMixin,  CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView( LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blo/about.html', {'title': 'About'})


