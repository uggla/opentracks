#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A module to do bla bla
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: René Ribaud <rene.ribaud@free.fr>
"""


from lxml import etree


doc = etree.parse('sample/tcx/2012-09-22-08-04-19.tcx')
#root = etree.Element("root")
print(etree.tostring(doc, pretty_print=True))
