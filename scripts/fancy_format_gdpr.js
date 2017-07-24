/**
 * FANCY FORMAT GDPR TEXT
 * @author Harshvardhan Pandit
 * @author me a.t. harshp dot com
 * LICENSE: MIT
 *
 * Using the data from gdpr.json, this script restructures the HTML to create
 * a hierarchical page that can be referenced by HTML id attributes
 */

// clear the body
$('body').empty();

// insert title and other items
$('body').append(
    $('<h1>', {
        'id': 'title',
        'class': 'title',
        'text': data.title + ' (' + data.abbrv + ')' 
    }));
$('body').append(
    $('<p>', {
        'id': 'about',
        'class': 'description',
        'text': data.about
    }));

// recitals
var element_recital = $('<div>', { 'id': 'recitals' });
element_recital.append(
    $('<h2>', {
        'class': 'recital-title',
        'text': 'Recitals'
    }));
data.recitals.map(function(recital) {
   element_recital.append(
      $('<p>', {
         'id': 'recital-' + recital.number,
         'class': 'recital',
         'text': '(' + recital.number + ') ' + recital.text
      })); 
});
$('body').append(element_recital);

//  chapters
data.chapters.map(function(chapter) {
    var element_chapter = $('<div>', {
        'id': 'chapter' + chapter.number,
        'class': 'chapter'
    });
    element_chapter.append(
        $('<h2>', {
            'class': 'chapter-title',
            'text': "Chapter " + chapter.number + " " + chapter.title
        }));

    // process entries in chapter
    // store the article handler so that it can be called on sections and
    // articles and reduces the things written in if-else blocks

    /**
     * handles article and creates elements
     * returns article div containing points and sub-points
     */
    var handler_article = function(article) {
        var element_article = $('<div>', {
            'id': 'article' + article.number,
            'class': 'article'
        });
        element_article.append(
            $('<h3>', {
                'class': 'article-title',
                'text': 'Article ' + article.number + " " + article.title
            }));
        // handle points
        article.contents.map(function(point) {
            if (point.number != null) {
                var element_point = $('<p>', {
                    'id': 'article' + article.number + '-' + point.number,
                    'class': 'point',
                    'text': '(' + point.number + ') ' + point.text
                });
            } else {
                var element_point = $('<p>', {
                    'class': 'point',
                    'text': point.text
                });
            }
            point.subpoints.map(function(subpoint) {
                if (subpoint.number != null) {
                    element_point.append(
                        $('<p>', {
                           'id': 'article' + article.number + '-' + point.number
                                + '-' + subpoint.number,
                           'class': 'subpoint',
                           'text': '(' + subpoint.number + ') ' + subpoint.text
                        })); 
                } else {
                    element_point.append(
                        $('<p>', {
                           'class': 'subpoint',
                           'text': '- ' + subpoint.text
                        })); 
                }
            });
            element_article.append(element_point);
        });
    
        return element_article;
    };
    // process sections if chapter has sections
    if (chapter.contents[0].type == 'section') {
        chapter.contents.map(function(section) {
            var element_section = $('<div>', {
                'id': 'section' + section.number,
                'class': 'section'
            });
            element_section.append(
                $('<h3>', {
                    'class': 'section-title',
                    'text': 'Section ' + section.number + " " + section.title
                }));
            section.contents.map(function(article) {
                element_section.append(handler_article(article));
            });
            element_chapter.append(element_section);
        });
    } else {
        chapter.contents.map(function(article) {
            element_chapter.append(handler_article(article));
        });
    }

    // append chapter to body
    $('body').append(element_chapter);
});

// Citations / References
var element_citation = $('<div>', { 'id': 'citations' });
element_citation.append(
    $('<h2>', {
        'class': 'citation-title',
        'text': 'References'
    }));
data.citations.map(function(index, citation) {
    element_citation.append(
      $('<p>', {
         'id': 'citation-' + citation.number,
         'class': 'citation',
         'text': '(' + citation.number + ') ' + citation.text
      })); 
});
$('body').append(element_citation);
