from django.contrib import admin
from .models import Category, Announcement


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
