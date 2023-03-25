from django.contrib import admin
from apps.blog.models import Category, Post
from parler.admin import TranslatableAdmin


class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )


class PostAdmin(TranslatableAdmin):
    list_display = ['title', 'created_at', 'is_featured', 'views']
    list_display_links = ['title']
    search_fields = ['title', 'author', 'description']
    list_per_page = 20
    list_filter = ['is_featured', 'categories']
    list_editable = ['is_featured']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'content','categories', 'image', 'is_featured', 'created_at', 'updated_at', 'views', 'slug'),
        },),
    )
    readonly_fields = ['views', 'slug']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

