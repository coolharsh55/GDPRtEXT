#!/usr/bin/env python3

# author: Harshvardhan Pandit

# Generates RDF graph for GDPR text from JSON (gdpr.json)
# The JSON file is in ../deliverables/gdpr.json
# The algorithm is roughly as follows:

# For every chapter, article, subpoint, et. al. it defines the following
# attributes using the ELI vocabulary
# @prefix ELI https://publications.europa.eu/en/mdr/resource/eli/eli.owl
#
# - ELI:title (xsd:string) title of the item
# - ELI:number (xsd:string) number of the item in text
# - ELI:TITLE_ALT (xsd:string) an alternative representation of the
#       item as <item_type> followed by <item_number>; e.g. Chapter 1
# - ELI:DESC (xsd:string) text of the item
# - ELI:PART_OF (ELI:LegalResource) gdpr:GDPR
#       here, this is an instance of a LegalResource created to represent
#       the GDPR, and is present in another OWL file, which is being edited
#       in Protege. The reference does not need to be resolved.
# - ELI:id_local (xsd:string) the ID of the resource in the HTML file
#       This is a bungling of the correct use of the vocabulary, but it keeps
#       all terms within the intended usage. The same ID can be used to
#       lookup the resource in the HTML file (so it is the ID attribute of
#       the resource).
#
# This script generates the RDF pairings for the text of the GDPR. The bulk
# of the work and the part where the GDPR itself is referenced is actually
# done using Protege, and does not need the use of a script, such as this,
# since it is a manual labour.

##############################################################################
from rdflib import Graph, RDF, RDFS, XSD, Literal, URIRef, BNode
from rdflib import Namespace

# Load the JSON from file
with open('../deliverables/gdpr.json') as fd:
    import json
    gdpr_json = json.load(fd)
    # import p# print
    # p# print.p# print(gdpr_json)
# This will be the graph used to hold the triples as they are being generated
graph = Graph()
GDPRtEXT_URI = URIRef('http://purl.org/adaptcentre/ontologies/GDPRtEXT#')
GDPRtEXT = Namespace(GDPRtEXT_URI)
graph.namespace_manager.bind('GDPRtext', GDPRtEXT)
DCTERMS = Namespace('http://purl.org/dc/terms/')
graph.namespace_manager.bind('dcterms', DCTERMS)
# This is the ELI namespace, used as the legal vocabulary for EU text
ELI = Namespace("http://data.europa.eu/eli/ontology#")
graph.namespace_manager.bind('eli', ELI)
# bind ELI items to names that are easier to access (argumentative)
LRS = ELI.LegalResourceSubdivision
TITLE = ELI.title
NOS = ELI.number
TITLE_ALT = ELI.title_alternative
PART_OF = ELI.is_part_of
# graph.add((PART_OF, RDF.type, OWL.TransitiveProperty))
DESC = ELI.description

##############################################################################
# GDPR as named individual
# base URI
GDPR_URI = URIRef('http://purl.org/adaptcentre/resources/GDPRtEXT#')
GDPR = Namespace(GDPR_URI)
graph.namespace_manager.bind('gdpr', GDPR)
gdpr = GDPR.GDPR
# graph.add((gdpr, RDF.type, OWL.NamedIndividual))
graph.add((gdpr, RDF.type, ELI.LR))
graph.add((gdpr, RDF.type, DCTERMS.Policy))
graph.add((gdpr, DCTERMS.identifier, Literal(
    '2016/679', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.language, Literal(
    'English', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.publisher, Literal(
    'Official Journal of the European Union', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.source, Literal(
    'http://eur-lex.europa.eu/eli/reg/2016/679/oj', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.title, Literal(
    'General Data Protection Regulation', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.title_alternative, Literal(
    'GDPR', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.title_alternative, Literal(
    'REGULATION (EU) 2016/679', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.creator, Literal(
    'European Parliament', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.creator, Literal(
    'Council of the European Union', datatype=XSD.string)))
graph.add((gdpr, DCTERMS.abstract, Literal((
    'REGULATION (EU) 2016/679 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL '
    'of 27 April 2016 '
    'on the protection of natural persons with regard to the processing of '
    'personal data and on the free movement of such data, '
    'and repealing Directive 95/46/EC '
    '(General Data Protection Regulation)'), datatype=XSD.string)))
gdpr_description = BNode()
graph.add((gdpr_description, RDF.type, RDF.Statement))
gdpr_description1 = BNode()
graph.add((gdpr_description1, RDF.type, RDF.Statement))
graph.add((gdpr_description1, DCTERMS.description, Literal((
    'THE EUROPEAN PARLIAMENT AND THE COUNCIL OF THE EUROPEAN UNION, '
    'Having regard to the Treaty on the Functioning of the European Union, '
    'and in particular Article 16 thereof, Having regard to the proposal from '
    'the European Commission, After transmission of the draft legislative act '
    'to the national parliaments,'), datatype=XSD.string)))
graph.add((gdpr_description1, DCTERMS.isPartOf, gdpr_description))
graph.add((gdpr_description, DCTERMS.hasPart, gdpr_description1))
gdpr_description2 = BNode()
graph.add((gdpr_description2, RDF.type, RDF.Statement))
graph.add((gdpr_description2, DCTERMS.description, Literal((
    'Having regard to the opinion of the European Economic '
    'and Social Committee,'), datatype=XSD.string)))
graph.add((gdpr_description2, DCTERMS.isPartOf, gdpr_description))
graph.add((gdpr_description, DCTERMS.hasPart, gdpr_description2))
graph.add((gdpr_description2, DCTERMS.references, GDPR['citation1']))
graph.add((gdpr_description2, ELI.cites, GDPR['citation1']))
gdpr_description3 = BNode()
graph.add((gdpr_description3, RDF.type, RDF.Statement))
graph.add((gdpr_description3, DCTERMS.description, Literal(
    'Having regard to the opinion of the Committee of the Regions,',
    datatype=XSD.string)))
graph.add((gdpr_description3, DCTERMS.isPartOf, gdpr_description))
graph.add((gdpr_description, DCTERMS.hasPart, gdpr_description3))
graph.add((gdpr_description3, DCTERMS.references, GDPR['citation2']))
graph.add((gdpr_description3, ELI.cites, GDPR['citation2']))
graph.add((gdpr, DCTERMS.description, gdpr_description))
gdpr_description4 = BNode()
graph.add((gdpr_description4, RDF.type, RDF.Statement))
graph.add((gdpr_description4, DCTERMS.description, Literal(
    'Acting in accordance with the ordinary legislative procedure,',
    datatype=XSD.string)))
graph.add((gdpr_description4, DCTERMS.isPartOf, gdpr_description))
graph.add((gdpr_description, DCTERMS.hasPart, gdpr_description4))
graph.add((gdpr_description4, DCTERMS.references, GDPR['citation3']))
graph.add((gdpr_description4, ELI.cites, GDPR['citation3']))
graph.add((gdpr, DCTERMS.description, gdpr_description))
graph.add((gdpr, ELI.date_document, Literal('2016-04-27', datatype=XSD.date)))
graph.add((gdpr, DCTERMS.date, Literal('2016-04-27', datatype=XSD.date)))
graph.add((gdpr, ELI.date_publication, Literal(
    '2016-05-04', datatype=XSD.date)))
graph.add((gdpr, DCTERMS.issued, Literal('2016-05-04', datatype=XSD.date)))
graph.add((gdpr, ELI.in_force, Literal(
    '2016-05-24', datatype=XSD.date)))
graph.add((gdpr, ELI.date_applicability, Literal(
    '2018-05-25', datatype=XSD.date)))


class_Chapter = GDPRtEXT['Chapter']
class_Section = GDPRtEXT['Section']
class_Article = GDPRtEXT['Article']
class_Point = GDPRtEXT['Point']
class_SubPoint = GDPRtEXT['SubPoint']
class_Recital = GDPRtEXT['Recital']
class_Citation = GDPRtEXT['Citation']
property_partof_chapter = GDPRtEXT['isPartOfChapter']
property_partof_section = GDPRtEXT['isPartOfSection']
property_partof_article = GDPRtEXT['isPartOfArticle']
property_partof_point = GDPRtEXT['isPartOfPoint']

#############################################################################

# The chapters are in json.chapters as an array of dicts
# { NOS, title, contents }
# A chapter may contain sections, and if it does, then it has the same
# structure as well.
# If a chapter has sections, then the section, else the chapter itself, has
# several articles with the same structure.
# Each article has several points, which may or may not be numbered.
# Each point may have several points, which may or may not be numbered.


def graph_subpoint(
        subpoint, article_number, point_number,
        point, article, section=None, chapter=None):
    '''adds subpoint to graph'''
    # print('SP', subpoint['number'])
    node_subpoint = GDPR['article{}-{}-{}'.format(
        article_number, point_number, subpoint['number'])]
    graph.add((node_subpoint, NOS, Literal(
        subpoint['number'], datatype=XSD.string)))
    graph.add((node_subpoint, TITLE_ALT, Literal(
        'Article' + article_number + '({})({})'.format(
            point_number, subpoint['number']),
        datatype=XSD.string)))
    graph.add((node_subpoint, RDF.type, LRS))
    graph.add((node_subpoint, RDF.type, class_SubPoint))
    graph.add((node_subpoint, PART_OF, chapter))
    graph.add((node_subpoint, property_partof_chapter, chapter))
    if section is not None:
        graph.add((node_subpoint, PART_OF, section))
        graph.add((node_subpoint, property_partof_section, section))
    graph.add((node_subpoint, PART_OF, article))
    graph.add((node_subpoint, property_partof_article, article))
    graph.add((node_subpoint, PART_OF, point))
    graph.add((node_subpoint, property_partof_point, point))
    graph.add((node_subpoint, PART_OF, gdpr))
    graph.add((node_subpoint, DESC, Literal(
        subpoint['text'], datatype=XSD.string)))


def graph_point(point, article_number, article, section=None, chapter=None):
    '''adds point to graph'''
    # print('P', point['number'])
    node_point = GDPR['article{}-{}'.format(
        article_number, point['number'])]
    graph.add((node_point, NOS, Literal(
        point['number'], datatype=XSD.string)))
    graph.add((node_point, TITLE_ALT, Literal(
        'Article' + article_number + '({})'.format(point['number']),
        datatype=XSD.string)))
    graph.add((node_point, RDF.type, LRS))
    graph.add((node_point, RDF.type, class_Point))
    graph.add((node_point, PART_OF, chapter))
    graph.add((node_point, property_partof_chapter, chapter))
    if section is not None:
        graph.add((node_point, PART_OF, section))
        graph.add((node_point, property_partof_section, section))
    graph.add((node_point, PART_OF, article))
    graph.add((node_point, property_partof_article, article))
    graph.add((node_point, PART_OF, gdpr))
    graph.add((node_point, DESC, Literal(
        point['text'], datatype=XSD.string)))
    # subpoint number to be used only when they are un-numbered
    subpoint_nos = 1
    for subpoint in point['subpoints']:
        if subpoint['number'] is None:
            subpoint['number'] = subpoint_nos
            subpoint_nos += 1
        graph_subpoint(
                subpoint, article_number, point['number'],
                node_point, article, section, chapter)


def graph_article(article, section=None, chapter=None):
    '''adds article to graph'''
    # print('A', article['number'])
    node_article = GDPR['article{}'.format(article['number'])]
    graph.add((node_article, RDF.type, LRS))
    graph.add((node_article, RDF.type, class_Article))
    graph.add((node_article, NOS, Literal(
        article['number'], datatype=XSD.string)))
    graph.add((node_article, TITLE_ALT, Literal(
        'Article ' + article['number'], datatype=XSD.string)))
    graph.add((node_article, PART_OF, chapter))
    graph.add((node_article, property_partof_chapter, chapter))
    graph.add((node_article, PART_OF, gdpr))
    if section is not None:
        graph.add((node_article, PART_OF, section))
        graph.add((node_article, property_partof_section, section))
    # point number for when points are unnumbered
    point_nos = 1
    for point in article['contents']:
        if point['number'] is None:
            point['number'] = point_nos
            point_nos += 1
        graph_point(point, article['number'], node_article, section, chapter)


def graph_section(section, chapter, chapter_number):
    '''adds section to graph'''
    # print('S', section['number'], section['title'])
    node_section = GDPR[
            'chapter{}-{}'.format(chapter_number, section['number'])]
    graph.add((node_section, RDF.type, LRS))
    graph.add((node_section, RDF.type, class_Section))
    graph.add((node_section, TITLE, Literal(
        section['title'], datatype=XSD.string)))
    graph.add((node_section, NOS, Literal(
        section['number'], datatype=XSD.string)))
    graph.add((node_section, TITLE_ALT, Literal(
        'Section ' + section['number'], datatype=XSD.string)))
    graph.add((node_section, PART_OF, chapter))
    graph.add((node_section, PART_OF, gdpr))
    graph.add((node_section, property_partof_chapter, chapter))
    for article in section['contents']:
        graph_article(article, node_section, chapter)


def graph_chapter(chapter):
    '''adds chapter to graph'''
    # print('C', chapter['number'], chapter['title'])
    node_chapter = GDPR['chapter{}'.format(chapter['number'])]
    graph.add((node_chapter, RDF.type, LRS))
    graph.add((node_chapter, RDF.type, class_Chapter))
    graph.add((node_chapter, TITLE, Literal(
        chapter['title'], datatype=XSD.string)))
    graph.add((node_chapter, NOS, Literal(
        chapter['number'], datatype=XSD.string)))
    graph.add((node_chapter, TITLE_ALT, Literal(
        'Chapter ' + chapter['number'], datatype=XSD.string)))
    graph.add((node_chapter, PART_OF, gdpr))

    contents = chapter['contents']
    # Section (if any)
    if contents[0]['type'] == 'section':
        for item in contents:
            graph_section(item, node_chapter, chapter['number'])
    else:
        for item in contents:
            graph_article(item, None, node_chapter)


for chapter in gdpr_json['chapters']:
    graph_chapter(chapter)


for recital in gdpr_json['recitals']:
    node_recital = GDPR['recital{}'.format(recital['number'])]
    graph.add((node_recital, RDF.type, LRS))
    graph.add((node_recital, RDF.type, class_Recital))
    graph.add((node_recital, NOS, Literal(
        recital['number'], datatype=XSD.string)))
    graph.add((node_recital, DESC, Literal(
        recital['text'], datatype=XSD.string)))
    graph.add((node_recital, PART_OF, gdpr))


for citation in gdpr_json['citations'].values():
    node_citation = GDPR['citation{}'.format(citation['number'])]
    graph.add((node_citation, RDF.type, LRS))
    graph.add((node_citation, RDF.type, class_Citation))
    graph.add((node_citation, NOS, Literal(
        citation['number'], datatype=XSD.string)))
    graph.add((node_citation, DESC, Literal(
        citation['text'], datatype=XSD.string)))
    graph.add((node_citation, PART_OF, gdpr))


# Add citations
graph.add((GDPR['recital3'], ELI.cites, GDPR['citation4']))
graph.add((GDPR['recital13'], ELI.cites, GDPR['citation5']))
graph.add((GDPR['recital17'], ELI.cites, GDPR['citation6']))
graph.add((GDPR['recital19'], ELI.cites, GDPR['citation7']))
graph.add((GDPR['recital21'], ELI.cites, GDPR['citation8']))
graph.add((GDPR['recital35'], ELI.cites, GDPR['citation9']))
graph.add((GDPR['recital42'], ELI.cites, GDPR['citation10']))
graph.add((GDPR['recital54'], ELI.cites, GDPR['citation11']))
graph.add((GDPR['recital106'], ELI.cites, GDPR['citation12']))
graph.add((GDPR['recital147'], ELI.cites, GDPR['citation13']))
graph.add((GDPR['recital154'], ELI.cites, GDPR['citation14']))
graph.add((GDPR['recital161'], ELI.cites, GDPR['citation15']))
graph.add((GDPR['recital163'], ELI.cites, GDPR['citation16']))
graph.add((GDPR['recital172'], ELI.cites, GDPR['citation17']))
graph.add((GDPR['recital173'], ELI.cites, GDPR['citation18']))
graph.add((GDPR['article4-25'], ELI.cites, GDPR['citation19']))
graph.add((GDPR['article43-1-2'], ELI.cites, GDPR['citation20']))
graph.add((GDPR['article76-2'], ELI.cites, GDPR['citation21']))

# Serialize
graph.serialize(destination='../deliverables/gdpr.ttl', format='turtle')
graph.serialize(destination='../deliverables/gdpr.rdf', format='pretty-xml')
graph.serialize(destination='../deliverables/gdpr.n3', format='n3')
graph.serialize(destination='../deliverables/gdpr.nt', format='nt')
graph.serialize(destination='../deliverables/gdpr.jsonld', format='json-ld')
