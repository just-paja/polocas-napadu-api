from graphene import Field, String

from graphene_django.types import DjangoObjectType

from fields import serialize_image_field

from .models import Article, Chapter, ChapterPhoto


class ChapterPhotoNode(DjangoObjectType):
    class Meta:
        model = ChapterPhoto

    def resolve_image(self, info, *_):
        return serialize_image_field(self.image, info)


class ChapterNode(DjangoObjectType):
    class Meta:
        model = Chapter


class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article

    def resolve_chapters(self, info, *_):
        return self.chapters.get_visible().order_by("weight")


class Query:
    article = Field(ArticleNode, slug=String())
    anchored_article = Field(ArticleNode, site_anchor=String())

    def resolve_article(self, info, slug):
        try:
            return Article.objects.get_visible().filter(slug=slug).first()
        except Article.DoesNotExist:
            return None

    def resolve_anchored_article(self, info, site_anchor):
        try:
            return Article.objects.get_visible().filter(site_anchor=site_anchor).first()
        except Article.DoesNotExist:
            return None
