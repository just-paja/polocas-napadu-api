from fields.admin import BaseAdminModel, BaseInlineAdminModel, BaseStackedAdminModel

from .models import Article, Chapter, ChapterPhoto


class ChapterPhotoAdmin(BaseInlineAdminModel):
    model = ChapterPhoto


class ChapterAdmin(BaseAdminModel):
    model = Chapter
    inlines = [
        ChapterPhotoAdmin,
    ]
    fields = ('article', 'name', 'visibility', 'description', 'slug')
    list_display = ('name', 'article', 'visibility')
    list_filter = ('visibility', 'article')
    readonly_fields = ('slug',)
    search_fields = ('name', 'description')


class ChapterInlineAdmin(BaseStackedAdminModel):
    model = Chapter
    fields = ('name', 'visibility', 'description')
    inlines = [
        ChapterPhotoAdmin,
    ]


class ArticleAdmin(BaseAdminModel):
    model = Article
    fields = ('name', 'visibility', 'site_anchor', 'description', 'slug')
    list_display = ('name', 'site_anchor', 'visibility')
    list_filter = ('visibility', 'site_anchor')
    readonly_fields = ('slug',)
    search_fields = ('name', 'description')
    inlines = [
        ChapterInlineAdmin,
    ]
