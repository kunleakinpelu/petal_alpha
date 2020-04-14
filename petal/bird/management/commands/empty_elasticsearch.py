from django.conf import settings
from django.core.management.base import BaseCommand

from elasticsearch import Elasticsearch


class Command(BaseCommand):
    args = 'None.'

    def empty_elasticsearch(self):
        if not settings.DEBUG:
            print(self.help)
            return
        es = Elasticsearch(settings.ELASTIC_SEARCH_HOST)
        es.indices.delete(index='_all', ignore=[400, 404])
        es.indices.create(index='tags')
        es.indices.create(index='petal-search-base')
        es.indices.create(index='petal-search-user-specific-1')
        print ("Emptied all data")

    def handle(self, *args, **options):
        self.empty_elasticsearch()