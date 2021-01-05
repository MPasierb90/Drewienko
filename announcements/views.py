from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Announcement
from django.contrib.auth.models import User

class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    template_name = "portal_v1/announcement_form.html"
    fields = ['title', 'picture', 'content', 'city', 'price', 'category', 'shipping', 'sell_or_exchange']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'portal_v1/home.html'
    context_object_name = 'ann_items'
    ordering = ['-date_posted']

class MyAnnouncementListView(ListView):
    model = Announcement
    template_name = 'portal_v1/my_announcements.html'
    context_object_name = 'my_ann_items'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Announcement.objects.filter(author=self.request.user )

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
