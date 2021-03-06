#!/usr/bin/env python
from datetime import datetime
from unittest import TestCase

from solar.util import X, make_fq

class UtilTest(TestCase):
    def test_X(self):
        self.assertEqual(unicode(X(status=0)),
                         u"(AND: ('status', 0))")
        self.assertEqual(unicode(X(status=0) & X(company_status__in=[0,6])),
                         u"(AND: ('status', 0), ('company_status__in', [0, 6]))")
        self.assertEqual(unicode(X(status=0) | X(company_status=0)),
                         u"(OR: ('status', 0), ('company_status', 0))")
        self.assertEqual(unicode(X(with_photo=True)),
                         u"(AND: ('with_photo', True))")
        self.assertEqual(unicode(X(date_created__gt=datetime(2012, 5, 17, 14, 35, 41, 794880))),
                         u"(AND: ('date_created__gt', datetime.datetime(2012, 5, 17, 14, 35, 41, 794880)))")
        self.assertEqual(unicode(X(price__lt=1000)),
                         u"(AND: ('price__lt', 1000))")
        self.assertEqual(unicode(X(price__gte=100) & X(price__lte=1000)),
                         u"(AND: ('price__gte', 100), ('price__lte', 1000))")
        self.assertEqual(unicode(X(price__between=[500, 1000])),
                         u"(AND: ('price__between', [500, 1000]))")
        self.assertEqual(unicode(X(category__in=[1, 2, 3, 4, 5]) & (X(status=0) | X(status=5) | X(status=1) & X(company_status=6))),
                         u"(AND: ('category__in', [1, 2, 3, 4, 5]), (OR: ('status', 0), ('status', 5), (AND: ('status', 1), ('company_status', 6))))")
        self.assertEqual(unicode(~X(status=1)),
                         u"(AND: (NOT (AND: ('status', 1))))")
        self.assertEqual(unicode(~X(status__in=[1, 2, 3])),
                         u"(AND: (NOT (AND: ('status__in', [1, 2, 3]))))")
    
    def test_make_fq(self):
        self.assertEqual(make_fq(X(status=0)),
                         u"status:0")
        self.assertEqual(make_fq(X(status=0) & X(company_status__in=[0,6])),
                         u"status:0 AND (company_status:0 OR company_status:6)")
        self.assertEqual(make_fq(X(status=0) | X(company_status=0)),
                         u"(status:0 OR company_status:0)")
        self.assertEqual(make_fq(X(with_photo=True)),
                         u"with_photo:1")
        self.assertEqual(make_fq(X(date_created__gt=datetime(2012, 5, 17, 14, 35, 41, 794880))),
                         u"date_created:{2012-05-17T14:35:41Z TO *}")
        self.assertEqual(make_fq(X(price__lt=1000)),
                         u"price:{* TO 1000}")
        self.assertEqual(make_fq(X(price__gte=100) & X(price__lte=1000)),
                         u"price:[100 TO *] AND price:[* TO 1000]")
        self.assertEqual(make_fq(X(price__between=[500, 1000])),
                         u"price:[500 TO 1000]")
        self.assertEqual(make_fq(X(category__in=[1, 2, 3, 4, 5]) & (X(status=0) | X(status=5) | X(status=1) & X(company_status=6))),
                         u"(category:1 OR category:2 OR category:3 OR category:4 OR category:5) AND (status:0 OR status:5 OR (status:1 AND company_status:6))")
        self.assertEqual(make_fq(~X(status=1)),
                         u"(NOT status:1)")
        self.assertEqual(make_fq(~X(status__in=[1, 2, 3])),
                         u"(NOT (status:1 OR status:2 OR status:3))")
                 
if __name__ == '__main__':
    from unittest import main
    main()
