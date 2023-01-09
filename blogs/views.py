from django.views import generic, View
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone

from blogs.models import Post, Series, Category
from blogs.forms import PostCommentForm


class HomePageView(generic.ListView):
    # TODO: session for dark/light mode
    queryset = Post.objects.filter(
        pub_date__lte=timezone.now()
    )
    template_name = 'blogs/homepage.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['featured'] = self.queryset.filter(featured=True)[:3]
        return context


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.filter(
        pub_date__lte=timezone.now()
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCommentForm()
        return context


class PostCommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    # TODO: Allow user to reply to a comment
    # TODO: Allow edit/deletion of comment
    template_name = 'blogs/post_detail.html'
    form_class = PostCommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.post = self.object
        f.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:post', kwargs={'slug': self.object.slug}) + '#comments-section'


class PostView(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)


class SeriesListView(generic.ListView):
    model = Series
    paginate_by = 10


class SeriesDetailView(generic.DetailView):
    model = Series


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10


class CategoryView(generic.ListView):
    model = Post
    template_name = "blogs/category_view.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.path.replace("/category/", "")
        post_list = Post.objects.filter(
            categories__slug=query
        ).filter(
            pub_date__lte=timezone.now()
        ).distinct()
        return post_list


class SearchResultsView(generic.ListView):
    model = Post
    template_name = "blogs/search_results.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("search")
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query)
        ).filter(
            pub_date__lte=timezone.now()
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search')
        return context
