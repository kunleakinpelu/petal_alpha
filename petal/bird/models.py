from django.core.cache import cache
from django.utils.text import slugify
from api.models import PetalObject, get_time
from neo4j import CypherError

from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, BooleanProperty, StructuredRel,
                      DateTimeProperty, RelationshipTo, Relationship,
                      db, DoesNotExist)


class Impression(StructuredRel):
    viewed = DateTimeProperty(default=get_time)
    view_count = IntegerProperty(default=0)


class ResultRel(StructuredRel):
    date_accessed = DateTimeProperty()


class KeywordRel(StructuredRel):
    relevance = FloatProperty(default=0)


class Keyword(StructuredNode):
    keyword = StringProperty()
    weight = IntegerProperty(default=0)

    # relationships
    queries = RelationshipTo('bird.models.Query', 'SEARCH_QUERY')


class Result(PetalObject):
    result_id = StringProperty(unique_index=True)
    object_type = StringProperty()

    # relationships
    queries = RelationshipTo('bird.models.Query', 'QUERY')
    clicked_by = RelationshipTo('petalusers.models.PetalUser', 'ACCESSED_BY',
                                model=ResultRel)


class Query(StructuredNode):
    weight = IntegerProperty(default=0)
    search_query = StringProperty(unique_index=True)
    search_count = IntegerProperty(default=1)
    last_searched = DateTimeProperty(default=get_time)
    trending = BooleanProperty(default=False)

    # relationships
    searched_by = Relationship('petalusers.models.PetalUser', 'SEARCHED_BY')
    # keywords = RelationshipTo(Keyword, 'KEYWORDS', model=KeywordRel)
    results = RelationshipTo(Result, 'RESULT')


class Searchable(PetalObject):
    search_id = StringProperty()
    populated_es_index = BooleanProperty(default=False)
    view_count = IntegerProperty(default=0)
    # summary = StringProperty()

    # relationships
    viewed_by = RelationshipTo('petalusers.models.PetalUser', "VIEWED_BY",
                               model=Impression)

    def get_search_count(self):
        return self.search_count

    # ensure the view count doesn't get too big
    def increment_search_count(self):
        try:
            if self.search_count >= 9223372036854775807:
                return 9223372036854775807
            self.search_count += 1
            self.save()
            return self.search_count
        except IndexError:
            return 0


class Article(Searchable):
    # __abstract_node__ = True
    __label__ = "Article"

    summary = StringProperty()
    images = StringProperty()
    references = StringProperty()
    links = StringProperty()
    title = StringProperty()
    content = StringProperty()
    longitude = FloatProperty()
    latitude = FloatProperty()
    # node_id = StringProperty(index = True)

    # Relationships
    article_relationship = Relationship(".article.Article", None)
    species_relationship = RelationshipTo(".species.Species", "MENTIONED_IN_ARTICLE")

    @classmethod
    def get(cls, object_uuid):
        article = cache.get(object_uuid)
        if article is None:
            response, _ = db.cypher_query(
                "MATCH (a:%s {object_uuid:'%s'}) RETURN a" % (
                    cls.__name__, object_uuid))
            try:
                try:
                    response[0][0].pull()
                except(CypherError, Exception):
                    pass
                article = cls.inflate(response[0][0])
            except IndexError:
                raise DoesNotExist('Article with id: %s '
                                   'does not exist' % object_uuid)
            cache.set(object_uuid, article)
        return article

class WikipediaArticle(Article):
    __label__ = "WikipediaArticle"
    pass

class Species(Searchable):
    Order = StringProperty()
    CatalogSource = StringProperty()
    Phylum = StringProperty()
    Genus = StringProperty()
    Family = StringProperty()
    Class = StringProperty()
    Name = StringProperty(required=True)
    # node_id = StringProperty(index = True)

    # Relationships (edges
    species_relationship = Relationship(".species.Species", None)
    article_relationship = RelationshipTo(".article.Article", "MENTIONS_SPECIES")

    @classmethod
    def get(cls, object_uuid):
        species = cache.get(object_uuid)
        if species is None:
            response, _ = db.cypher_query(
                "MATCH (a:%s {object_uuid:'%s'}) RETURN a" % (
                    cls.__name__, object_uuid))
            try:
                try:
                    response[0][0].pull()
                except(CypherError, Exception):
                    pass
                species = cls.inflate(response[0][0])
            except IndexError:
                raise DoesNotExist('Species with id: %s '
                                   'does not exist' % object_uuid)
            cache.set(object_uuid, species)
        return species

def get_parent_entity(object_uuid):
    try:
        query = 'MATCH (s:Searchable {object_uuid:"%s"}) RETURN s' % (
            object_uuid)
        res, col = db.cypher_query(query)
        try:
            content = Searchable.inflate(res[0][0])
        except ValueError:
            content = Searchable.inflate(res[0][0][0])
        return content
    except(CypherError, IOError, IndexError) as e:
        return e
