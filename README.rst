=====
Solar
=====

Library to use Solr with python.

Features
--------

1. Searching::

    searcher = SolrSearcher() # you can't do real requests to Solr, use next: SolrSearcher('http://localhost:8180/db')
    q = searcher.search('test', category=1).ps(5).qf('name^5 description').bf('linear(rank,100,0)')

    q=test+AND+category:1&ps=5&bf=linear(rank,100,0)&qf=name^5+description

2. Filtering::

    q = q.filter(status=0).filter(category__in=[1, 2, 3]).exclude(rank__lte=5)

    fq={!tag=status}status:0&fq={!tag=category}(category:1+OR+category:2+OR+category:3)&fq={!tag=rank}-rank:[*+TO+5]

    q = q.exclude(rank=None)

    fq={!tag=rank}rank:[*+TO+*]

3. Grouping::

    q = q.group('director', limit=5)

    group=true&group.ngroups=true&group.field=director&group.limit=5

4. Facets::

    q = q.facet('status').facet(['category', 'type'], params={'category': {'mincount': 5}})

    facet.mincount=1&facet.sort=true&facet.field={!ex=status}status&facet.field={!ex=category}category&facet.field={!ex=type}type&facet.missing=false&facet.offset=0&facet.method=fc&facet=true&facet.limit=-1&f.category.facet.mincount=5

    qf = q.get_query_filter()
    qf.add_ordering([(u'by rank', '-rank'), (u'by date', '-date_created')])
    # now you can filter your search query by get parameters
    # supports Django's QueryDict, webob's MultiDict or python dict
    q = qf.apply(q, {'status': [0,1], 'type': 3, 'type__gte': 5, 'sort': '-rank'})

    fq={!tag=rank}-rank:[*+TO+*]&fq={!tag=status}(status:0+OR+status:1)&sort=rank+desc

There are facet.field and facet.query support.
Also automatically adds tag for every fq and excludes corresponding fq's from facets.
See http://wiki.apache.org/solr/SimpleFacetParameters#Multi-Select_Faceting_and_LocalParams

5. Mapping

Mapping docs and facets on any objects you want
and then you can access it via .instance attribute::

    class MovieSearcher(SolrSearcher):
        model = Movie

        # example of non-standart mapping
        class KeywordFacet(Facet):
            field = 'keywords'
            model = Keyword
            session = session

            def get_id(self, id):
                return id

            def get_instances(self, ids):
                return dict([(obj.name, obj) for obj in session.query(self.model).filter(self.model.name.in_(ids)])

        def get_instances(self, ids):
            return dict([(obj.id, obj) for obj in session.query(self.model).filter(self.model.id.in_(ids)])
    
    q = Movie.searcher.search(u'monty python').facet('keywords')
    for doc in q:
        print doc.instance.id, doc.instance.name

    for fv in q.results.get_facet('keywords'):
        print fv.instance.name, fv.count
  
6. Multiple Solr's

Reading from and writing to multiple Solr instances.
For reading choses Solr instance randomly.
Writes into every Solr instance.
You should syncronize reading Solr's with writing instances manually (use rsync or something else).

7. Lazy evaluate

Only iterating, count and access to .results attribute make http requests to Solr.

TODO
----

* Dynamic fields support (need mapping for facets)
* Groups refactoring
* Lazy results and facets
* facet.date and facet.range support
* Django support
* Documentation
* Unit tests
