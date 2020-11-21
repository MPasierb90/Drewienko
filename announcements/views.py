from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Announcement, Category


class Pagination:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'&q={self.request.GET.get("q")}'
        return context


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    template_name = "portal_v1/announcement_form.html"
    fields = ['title', 'picture', 'content', 'city', 'price', 'category', 'shipping', 'sell_or_exchange']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryListView(ListView):
    model = Category

    def get(self, request):
        all_categories = Category.objects.all()
        context = {'all_categories': all_categories}
        return render(request, 'portal_v1/home.html', context)


class AnnouncementListView(Pagination, ListView):
    model = Announcement
    template_name = 'portal_v1/home.html'
    context_object_name = 'ann_items'
    ordering = ['-date_posted']
    paginate_by = 2  # dzielenie calej listy ogloszen na strony po 2 ogloszenia


def main_page(request):
    all_categories = Category.objects.all()
    all_announcements = Announcement.objects.all().order_by('-date_posted')
    return render(request, 'portal_v1/home.html', {'all_categories': all_categories, 'ann_items': all_announcements})


def announcements_by_category(request, name):
    all_announcements = Announcement.objects.filter(category__name=name)
    all_categories = Category.objects.all()
    return render(request, 'portal_v1/home.html', {'all_categories': all_categories, 'ann_items': all_announcements})


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'portal_v1/announcement_detail.html'


class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    fields = ['title', 'picture', 'content', 'city', 'price', 'category', 'shipping',
              'sell_or_exchange']
    template_name = "portal_v1/announcement_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ann = self.get_object()
        if self.request.user == ann.author:
            return True
        return False


class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = "portal_v1/announcement_confirm_delete.html"
    success_url = "/"

    def test_func(self):
        ann = self.get_object()
        if self.request.user == ann.author:
            return True
        return False


class SearchResultsView(Pagination, ListView):
    model = Announcement
    context_object_name = 'ann_items'
    template_name = 'portal_v1/search.html'
    paginate_by = 3

    def get_queryset(self):
        return Announcement.objects.filter(title__icontains=self.request.GET.get("q")).order_by('-date_posted')


class FilterAnnouncementList(CategoryListView):
    def get_queryset(self):
        queryset = Announcement.objects.filter(category=self.request.GET.get('category'))
        return queryset
