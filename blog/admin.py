from fields.admin import BaseAdminModel, BaseInlineAdminModel, BaseStackedAdminModel

from .models import Article, Chapter, ChapterPhoto, Poem


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
    fields = ('name', 'weight', 'visibility', 'description')
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


class PoemAdmin(BaseAdminModel):
    model = Poem
    fields = (
        'author',
        'name',
        'description',
        'visibility',
        'weight',
        'slug',
        'created',
        'modified'
    )
    list_display = ('name', 'author', 'visibility', 'weight', 'created', 'modified')
    list_filter = ('author', 'visibility')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('name', 'description')
    ordering = ('weight',)
