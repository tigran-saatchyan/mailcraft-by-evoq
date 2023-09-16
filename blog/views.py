import random
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, \
    DetailView, ListView
from pytils.translit import slugify

from blog.forms import PostForm
from blog.models import Posts


class PostSlugifyMixin:
    """
    A mixin for slugging post titles.

    This mixin is responsible for generating a unique slug for posts based on their titles.
    If a slug already exists, it appends a count to ensure uniqueness.
    """

    def form_valid(self, form):
        """
        Override the form_valid method to generate and assign a unique slug to the post.

        Args:
            form (PostForm): The form object containing post data.

        Returns:
            HttpResponse: The response after successfully saving the form.
        """
        post = form.save(commit=False)
        slug = slugify(post.title)
        post_objects = Posts.objects
        if post_objects.filter(slug=slug).exists():
            count = 1
            while post_objects.filter(slug=f'{slug}-{count}').exists():
                count += 1
            slug = f'{slug}-{count}'

        post.slug = slug
        post.save()
        return super().form_valid(form)


class PostListView(ListView):
    """
    View for listing blog posts.

    Attributes:
        model (Posts): The model associated with this view.
        context_object_name (str): The name of the variable to use in the template for the list of posts.
        template_name (str): The name of the template to render.
        ordering (tuple): The default ordering for the posts.

    Methods:
        get_paginate_by: Set the number of posts per page based on user authentication.
        get_queryset: Filter posts based on user authentication.
        get_context_data: Add additional context data for the template.
    """
    model = Posts
    context_object_name = 'posts'
    template_name = 'blog/posts_list.html'
    ordering = ('-creation_date',)

    def get_paginate_by(self, queryset):
        """
        Set the number of posts per page based on user authentication.

        Args:
            queryset: The queryset of posts.

        Returns:
            int: The number of posts to display per page.
        """
        if self.request.user.is_authenticated:
            paginate_by = 10
        else:
            paginate_by = 3
        return paginate_by

    def get_queryset(self):
        """
        Filter posts based on user authentication.

        Returns:
            queryset: The filtered queryset of posts.
        """
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            result = queryset.filter(user=self.request.user)
        else:
            result = queryset.filter(is_published=True)
        return result

    def get_context_data(self, *args, **kwargs):
        """
        Add additional context data for the template.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The updated context data.
        """
        context = super().get_context_data(*args, **kwargs)
        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)
        random.seed(int(current_date.timestamp() * 1000))

        last_month_posts = list(
            Posts.objects.filter(
                creation_date__gte=thirty_days_ago,
                is_published=True
            ).all()
        )

        featured_posts = Posts.objects.order_by('-views_count').filter(
            creation_date__gte=thirty_days_ago,
            is_published=True
        ).all()[:2]
        random_three_posts = random.sample(last_month_posts, 3)
        context.update(
            {
                'featured_posts': featured_posts,
                'random_three_posts': random_three_posts
            }
        )
        return context


class PostDetailView(DetailView):
    """
    View for displaying a single blog post.

    Attributes:
        model (Posts): The model associated with this view.
        context_object_name (str): The name of the variable to use in the template for the post.
        template_name (str): The name of the template to render.
        slug_url_kwarg (str): The name of the URL keyword argument for the post slug.

    Methods:
        get_object: Override to increment the views count of the post.
    """
    model = Posts
    context_object_name = 'post'
    template_name = 'blog/posts_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        """
        Override to increment the views count of the post.

        Args:
            queryset: The queryset of posts.

        Returns:
            Post: The post object.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1

        # TODO: Implement email notification
        #       service.utils.view_counter_email_notification
        self.object.save()

        return self.object


class PostCreateView(LoginRequiredMixin, PostSlugifyMixin, CreateView):
    """
    View for creating a new blog post.

    Attributes:
        model (Posts): The model associated with this view.
        template_name (str): The name of the template to render.
        slug_url_kwarg (str): The name of the URL keyword argument for the post slug.
        form_class (PostForm): The form class to use for creating a new post.

    Methods:
        get_success_url: Define the URL to redirect to after successful post creation.
        form_valid: Override to assign the user to the post before saving.
    """
    model = Posts
    template_name = 'blog/posts_form.html'
    slug_url_kwarg = 'slug'
    form_class = PostForm

    def get_success_url(self):
        """
        Define the URL to redirect to after successful post creation.

        Returns:
            str: The URL to redirect to.
        """
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'slug': self.object.slug}
        )

    def form_valid(self, form):
        """
        Override to assign the user to the post before saving.

        Args:
            form (PostForm): The form object containing post data.

        Returns:
            HttpResponse: The response after successfully saving the form.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostSlugifyMixin, UpdateView):
    """
    View for updating an existing blog post.

    Attributes:
        model (Posts): The model associated with this view.
        template_name (str): The name of the template to render.
        slug_url_kwarg (str): The name of the URL keyword argument for the post slug.
        context_object_name (str): The name of the variable to use in the template for the post.
        form_class (PostForm): The form class to use for updating the post.

    Methods:
        get_success_url: Define the URL to redirect to after successful post update.
    """
    model = Posts
    template_name = 'blog/posts_form.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    form_class = PostForm

    def get_success_url(self):
        """
        Define the URL to redirect to after successful post update.

        Returns:
            str: The URL to redirect to.
        """
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'slug': self.object.slug}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a blog post.

    Attributes:
        model (Posts): The model associated with this view.
        context_object_name (str): The name of the variable to use in the template for the post.
        slug_url_kwarg (str): The name of the URL keyword argument for the post slug.
        success_url (str): The URL to redirect to after successful post deletion.
    """
    model = Posts
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:post_list')
