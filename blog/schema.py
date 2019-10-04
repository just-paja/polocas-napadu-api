from graphene import List

from graphene_django.types import DjangoObjectType

from .models import Article, Chapter, ChapterPhoto


class ChapterPhotoNode(DjangoObjectType):
    class Meta:
        model = ChapterPhoto


class ChapterNode(DjangoObjectType):
    class Meta:
        model = Chapter


class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article


class Query:
    list_articles = List(ArticleNode)

    def resolve_list_articles(self, info):
        return Article.objects.get_visible()
