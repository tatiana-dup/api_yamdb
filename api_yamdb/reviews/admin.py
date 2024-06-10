from django.contrib import admin

from reviews.models import Category, Genre, GenreTitle, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('slug',)


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'description', 'genre_list')
    list_display_links = ('name',)
    search_fields = ('name', 'category')
    list_filter = ('year', 'category')
    inlines = [GenreTitleInline]
