#!/usr/bin/env bash

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
# - ELI:title_alternative (xsd:string) an alternative representation of the
#       item as <item_type> followed by <item_number>; e.g. Chapter 1
# - ELI:description (xsd:string) text of the item
# - ELI:is_part_of (ELI:LegalResource) gdpr:GDPR
#       here, this is an instance of a LegalResource created to represent
#       the GDPR, and is present in another OWL file, which is being edited
#       in Protege. The reference does not need to be resolved.
# - ELI:id_local (xsd:string) the ID of the resource in the HTML file
#       This is a bungling of the proper use of the vocabulary, but it keeps
#       all terms within the intended usage. The same ID can be used to
#       lookup the resource in the HTML file (so it is the ID attribute of
#       the resource).
#
# This script generates the RDF pairings for the text of the GDPR. The bulk
# of the work and the part where the GDPR itself is referenced is actually
# done using Protege, and does not need the use of a script, such as this,
# since it is a manual labour.

##############################################################################

# Load the JSON from file
with open('../deliverables/gdpr.json') as fd:
    import json
    gdpr_json = json.load(fd)
    # import p# print
    # p# print.p# print(gdpr_json)

from rdflib import Graph, RDF, XSD, Literal, BNode
# This will be the graph used to hold the triples as they are being generated
graph = Graph()

from rdflib import Namespace
# This is the ELI namespace, used as the legal vocabulary for EU text
ELI = Namespace("http://data.europa.eu/eli/ontology#")
LRS = ELI.LegalResourceSubdivision
title = ELI.title
number = ELI.number
title_alternative = ELI.title_alternative
is_part_of = ELI.is_part_of
description = ELI.description
# This is the GDPR namespace used by the project
# NOTE: this is temporary
GDPR = Namespace("http://www.semanticweb.org/harsh/ontologies/GDPR#")
node_gdpr = GDPR.GDPR

##############################################################################

# The chapters are in json.chapters as an array of dicts
# { number, title, contents }
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
    if subpoint['number'] is not None:
        node_subpoint = GDPR['article{}-{}{}'.format(
            article_number, point_number, subpoint['number'])]
        graph.add((node_subpoint, number, Literal(
            subpoint['number'], datatype=XSD.string)))
        graph.add((node_subpoint, title_alternative, Literal(
            'Article' + article_number + '({}{})'.format(
                point_number, subpoint['number']),
            datatype=XSD.string)))
    else:
        node_subpoint = BNode()
    graph.add((node_subpoint, RDF.type, LRS))
    graph.add((node_subpoint, is_part_of, node_gdpr))
    graph.add((node_subpoint, is_part_of, chapter))
    if section is not None:
        graph.add((node_subpoint, is_part_of, section))
    graph.add((node_subpoint, is_part_of, article))
    graph.add((node_subpoint, is_part_of, point))
    graph.add((node_subpoint, description, Literal(
        subpoint['text'], datatype=XSD.string)))


def graph_point(point, article_number, article, section=None, chapter=None):
    '''adds point to graph'''
    # print('P', point['number'])
    if point['number'] is not None:
        node_point = GDPR['article{}-{}'.format(
            article_number, point['number'])]
        graph.add((node_point, number, Literal(
            point['number'], datatype=XSD.string)))
        graph.add((node_point, title_alternative, Literal(
            'Article' + article_number + '({})'.format(point['number']),
            datatype=XSD.string)))
    else:
        node_point = BNode()
    graph.add((node_point, RDF.type, LRS))
    graph.add((node_point, is_part_of, node_gdpr))
    graph.add((node_point, is_part_of, chapter))
    if section is not None:
        graph.add((node_point, is_part_of, section))
    graph.add((node_point, is_part_of, article))
    graph.add((node_point, description, Literal(
        point['text'], datatype=XSD.string)))
    for subpoint in point['subpoints']:
        graph_subpoint(
                subpoint, article_number, point['number'],
                node_point, article, section, chapter)


def graph_article(article, section=None, chapter=None):
    '''adds article to graph'''
    # print('A', article['number'])
    node_article = GDPR['article{}'.format(article['number'])]
    graph.add((node_article, RDF.type, LRS))
    graph.add((node_article, number, Literal(
        article['number'], datatype=XSD.string)))
    graph.add((node_article, title_alternative, Literal(
        'Article ' + article['number'], datatype=XSD.string)))
    graph.add((node_article, is_part_of, node_gdpr))
    graph.add((node_article, is_part_of, chapter))
    if section is not None:
        graph.add((node_article, is_part_of, section))
    for point in article['contents']:
        graph_point(point, article['number'], node_article, section, chapter)


def graph_section(section, chapter):
    '''adds section to graph'''
    # print('S', section['number'], section['title'])
    node_section = GDPR['section{}'.format(section['number'])]
    graph.add((node_section, RDF.type, LRS))
    graph.add((node_section, title, Literal(
        section['title'], datatype=XSD.string)))
    graph.add((node_section, number, Literal(
        section['number'], datatype=XSD.string)))
    graph.add((node_section, title_alternative, Literal(
        'Section ' + section['number'], datatype=XSD.string)))
    graph.add((node_section, is_part_of, node_gdpr))
    graph.add((node_section, is_part_of, chapter))
    for article in section['contents']:
        graph_article(article, node_section, chapter)


def graph_chapter(chapter):
    '''adds chapter to graph'''
    # print('C', chapter['number'], chapter['title'])
    node_chapter = GDPR['chapter{}'.format(chapter['number'])]
    graph.add((node_chapter, RDF.type, LRS))
    graph.add((node_chapter, title, Literal(
        chapter['title'], datatype=XSD.string)))
    graph.add((node_chapter, number, Literal(
        chapter['number'], datatype=XSD.string)))
    graph.add((node_chapter, title_alternative, Literal(
        'Chapter ' + chapter['number'], datatype=XSD.string)))
    graph.add((node_chapter, is_part_of, node_gdpr))

    contents = chapter['contents']
    # Section (if any)
    if contents[0]['type'] == 'section':
        for item in contents:
            graph_section(item, node_chapter)
    else:
        for item in contents:
            graph_article(item, None, node_chapter)


for chapter in gdpr_json['chapters']:
    graph_chapter(chapter)

graph.serialize(destination='gdpr.ttl', format='turtle')
