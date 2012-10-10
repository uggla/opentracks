#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A module to do bla bla
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: René Ribaud <rene.ribaud@free.fr>
"""


from lxml import etree
import StringIO


f = StringIO.StringIO('''\
<a:foo xmlns:a="http://codespeak.net/ns/test1"
       xmlns:b="http://codespeak.net/ns/test2">
   <b:bar>Text</b:bar>
</a:foo>''')

doc = etree.parse(f)
r = doc.xpath('//b:bar',
               namespaces={'t': 'http://codespeak.net/ns/test1',
                           'b': 'http://codespeak.net/ns/test2'})
print len(r)
print r[0].tag
print r[0].text

print(etree.tostring(doc, pretty_print=True))


doc2 = etree.parse('sample/tcx/2012-09-22-08-04-19.tcx')
NS = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
#doc2 = etree.parse('./bidouille3.tcx')
#r2 = doc.xpath('//Time',
#               namespaces={'tc': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
#                           'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
#                           'schemaLocation': 'http://www.garmin.com/xmlschemas/ProfileExtension/v1 http://www.garmin.com/xmlschemas/UserProfilePowerExtensionv1.xsd http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd http://www.garmin.com/xmlschemas/UserProfile/v2 http://www.garmin.com/xmlschemas/UserProfileExtensionv2.xsd' })

r2 = doc2.xpath('//tc:Trackpoint',
                namespaces={'tc': NS})
#r2 = doc2.xpath('//tc:Trackpoint',
#                namespaces={'tc': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'})

print len(r2)
for node in r2:
    print 'Time : ' + node.xpath("tc:Time",
                     namespaces={'tc': NS})[0].text
    try:
        print 'Latitude : ' + node.xpath("tc:Position/tc:LatitudeDegrees",
                          namespaces={'tc': NS})[0].text
        print 'Longitude : ' + node.xpath("tc:Position/tc:LongitudeDegrees",
                          namespaces={'tc': NS})[0].text
    except:
        pass

    print 'Altitude : ' + node.xpath("tc:AltitudeMeters",
                      namespaces={'tc': NS})[0].text
    print 'Distance : ' + node.xpath("tc:DistanceMeters",
                      namespaces={'tc': NS})[0].text
    print 'HeartRate : '+ node.xpath("tc:HeartRateBpm/tc:Value",
                      namespaces={'tc': NS})[0].text
    print '======================'
    
#print(etree.tostring(doc2, pretty_print=True))
