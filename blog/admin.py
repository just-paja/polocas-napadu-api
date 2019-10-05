from fields.admin import BaseAdminModel, BaseInlineAdminModel, BaseStackedAdminModel

from .models import Article, Chapter, ChapterPhoto


class ChapterPhotoAdmin(BaseInlineAdminModel):
    model = ChapterPhoto


class ChapterAdmin(BaseAdminModel):
    model = Chapter
    inlines = [
        ChapterPhotoAdmin,
    ]
    fields = ('article', 'name', 'weight', 'visibility', 'description', 'slug', 'modified')
    list_display = ('name', 'article', 'weight', 'visibility', 'modified')
    list_filter = ('visibility', 'article')
    readonly_fields = ('slug', 'modified')
    search_fields = ('name', 'description')
    ordering = ('weight',)


class ChapterInlineAdmin(BaseStackedAdminModel):
    model = Chapter
    fields = ('name', 'visibility', 'description')
    inlines = [
        ChapterPhotoAdmin,
    ]


class ArticleAdmin(BaseAdminModel):
    model = Article
    fields = ('name', 'visibility', 'site_anchor', 'description', 'slug', 'modified')
    list_display = ('name', 'site_anchor', 'visibility', 'modified')
    list_filter = ('visibility', 'site_anchor')
    readonly_fields = ('slug', 'modified')
    search_fields = ('name', 'description')
    ordering = ('-created',)
    inlines = [
        ChapterInlineAdmin,
    ]
