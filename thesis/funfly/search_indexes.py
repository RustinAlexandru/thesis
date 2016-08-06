from haystack import indexes
from models import Ninegag, Youtube, Joke


class NinegagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    points = indexes.IntegerField(model_attr='points')

    def get_model(self):
        return Ninegag


class YoutubeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Youtube


class JokeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Joke
