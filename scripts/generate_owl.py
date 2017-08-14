#!/usr/bin/env python3

# author: Harshvardhan Pandit

# Creates the OWL ontology for GDPRtEXT
# NOTE: EDIT LATER WITH PROTEGE

##############################################################################
from rdflib import Graph, RDF, RDFS, XSD, OWL, Literal, URIRef, BNode
from rdflib import Namespace

graph = Graph()
DC = Namespace('http://purl.org/dc/elements/1.1/')
graph.namespace_manager.bind('dc', DC)
graph.namespace_manager.bind('owl', OWL)
GDPRtEXT_URI = URIRef('http://purl.org/adaptcentre/ontologies/GDPRtEXT#')
GDPRtEXT = Namespace('http://purl.org/adaptcentre/ontologies/GDPRtEXT#')
graph.namespace_manager.bind('GDPRtext', GDPRtEXT)
graph.add((GDPRtEXT_URI, RDF.type, OWL.Ontology))
graph.add((GDPRtEXT_URI, RDFS.label, Literal(
    'GDPR text EXTensions', datatype=XSD.string)))
graph.add((GDPRtEXT_URI, DC.title, Literal(
    'GDPRtEXT', datatype=XSD.string)))
graph.add((GDPRtEXT_URI, OWL.versionInfo, Literal(
    '0.1', datatype=XSD.string)))
graph.add((GDPRtEXT_URI, DC.creator, Literal(
    'Harshvardhan J. Pandit', datatype=XSD.string)))
graph.add((GDPRtEXT_URI, DC.description, Literal((
    'This ontology extends the canonical (official) GDPR text '
    'with additional annotations'), datatype=XSD.string)))
graph.add((GDPRtEXT_URI, RDFS.comment, Literal(
    'This is an ontology to represent GDPR text as a set of RDF resources',
    datatype=XSD.string)))

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

# declare chapters, etc. as subclasses of LRS
class_Chapter = GDPRtEXT['Chapter']
graph.add((class_Chapter, RDF.type, OWL.Class))
graph.add((class_Chapter, RDFS.subClassOf, LRS))
graph.add((class_Chapter, RDFS.label, Literal('Chapter', datatype=XSD.string)))
graph.add((class_Chapter, RDFS.comment, Literal(
    'Chapter in GDPR text', datatype=XSD.string)))
# declare section, etc. as subclasses of LRS
class_Section = GDPRtEXT['Section']
graph.add((class_Section, RDF.type, OWL.Class))
graph.add((class_Section, RDFS.subClassOf, LRS))
graph.add((class_Section, RDFS.label, Literal('Section', datatype=XSD.string)))
graph.add((class_Section, RDFS.comment, Literal(
    'Section in GDPR text', datatype=XSD.string)))
# declare article, etc. as subclasses of LRS
class_Article = GDPRtEXT['Article']
graph.add((class_Article, RDF.type, OWL.Class))
graph.add((class_Article, RDFS.subClassOf, LRS))
graph.add((class_Article, RDFS.label, Literal('Article', datatype=XSD.string)))
graph.add((class_Article, RDFS.comment, Literal(
    'Article in GDPR text', datatype=XSD.string)))
# declare point, etc. as subclasses of LRS
class_Point = GDPRtEXT['Point']
graph.add((class_Point, RDF.type, OWL.Class))
graph.add((class_Point, RDFS.subClassOf, LRS))
graph.add((class_Point, RDFS.label, Literal('Point', datatype=XSD.string)))
graph.add((class_Point, RDFS.comment, Literal(
    'Point in GDPR text', datatype=XSD.string)))
# declare subpoint, etc. as subclasses of LRS
class_SubPoint = GDPRtEXT['SubPoint']
graph.add((class_SubPoint, RDF.type, OWL.Class))
graph.add((class_SubPoint, RDFS.subClassOf, LRS))
graph.add((class_SubPoint, RDFS.label, Literal(
    'SubPoint', datatype=XSD.string)))
graph.add((class_SubPoint, RDFS.comment, Literal(
    'SubPoint in GDPR text', datatype=XSD.string)))

# Regulation
class_Recital = GDPRtEXT['Recital']
graph.add((class_Recital, RDF.type, OWL.Class))
graph.add((class_Recital, RDFS.subClassOf, LRS))
graph.add((class_Recital, RDFS.label, Literal(
    'Regulation', datatype=XSD.string)))
graph.add((class_Recital, RDFS.comment, Literal(
    'Regulation in GDPR text', datatype=XSD.string)))

# Citation
class_Citation = GDPRtEXT['Citation']
graph.add((class_Citation, RDF.type, OWL.Class))
graph.add((class_Citation, RDFS.subClassOf, LRS))
graph.add((class_Citation, RDFS.label, Literal(
    'Citation', datatype=XSD.string)))
graph.add((class_Citation, RDFS.comment, Literal(
    'Citation in GDPR text', datatype=XSD.string)))

# PROPERTIES
property_partof_chapter = GDPRtEXT['isPartOfChapter']
graph.add((property_partof_chapter, RDF.type, OWL.ObjectProperty))
graph.add((property_partof_chapter, RDF.type, OWL.FunctionalProperty))
graph.add((property_partof_chapter, RDFS.subPropertyOf, PART_OF))
graph.add((property_partof_chapter, RDFS.domain, LRS))
graph.add((property_partof_chapter, RDFS.range, class_Chapter))
graph.add((property_partof_chapter, RDFS.label, Literal(
    'is part of Chapter', datatype=XSD.string)))
graph.add((property_partof_chapter, RDFS.comment, Literal(
    'represents a legal resource subdivision to be part of a chapter',
    datatype=XSD.string)))

property_partof_section = GDPRtEXT['isPartOfSection']
graph.add((property_partof_section, RDF.type, OWL.ObjectProperty))
graph.add((property_partof_section, RDF.type, OWL.FunctionalProperty))
graph.add((property_partof_section, RDFS.subPropertyOf, PART_OF))
graph.add((property_partof_section, RDFS.domain, LRS))
graph.add((property_partof_section, RDFS.range, class_Section))
graph.add((property_partof_section, RDFS.label, Literal(
    'is part of Section', datatype=XSD.string)))
graph.add((property_partof_section, RDFS.comment, Literal(
    'represents a legal resource subdivision to be part of a section',
    datatype=XSD.string)))

property_partof_article = GDPRtEXT['isPartOfArticle']
graph.add((property_partof_article, RDF.type, OWL.ObjectProperty))
graph.add((property_partof_article, RDF.type, OWL.FunctionalProperty))
graph.add((property_partof_article, RDFS.subPropertyOf, PART_OF))
graph.add((property_partof_article, RDFS.domain, LRS))
graph.add((property_partof_article, RDFS.range, class_Article))
graph.add((property_partof_article, RDFS.label, Literal(
    'is part of Article', datatype=XSD.string)))
graph.add((property_partof_article, RDFS.comment, Literal(
    'represents a legal resource subdivision to be part of a article',
    datatype=XSD.string)))

property_partof_point = GDPRtEXT['isPartOfPoint']
graph.add((property_partof_point, RDF.type, OWL.ObjectProperty))
graph.add((property_partof_point, RDF.type, OWL.FunctionalProperty))
graph.add((property_partof_point, RDFS.subPropertyOf, PART_OF))
graph.add((property_partof_point, RDFS.domain, LRS))
graph.add((property_partof_point, RDFS.range, class_Point))
graph.add((property_partof_point, RDFS.label, Literal(
    'is part of Point', datatype=XSD.string)))
graph.add((property_partof_point, RDFS.comment, Literal(
    'represents a legal resource subdivision to be part of a point',
    datatype=XSD.string)))

graph.serialize(destination='../deliverables/gdpr.owl', format='xml')
