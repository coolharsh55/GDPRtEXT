/**
 * Parse GDPR text
 * @author Harshvardhan Pandit me a.t. harshp.com
 * @name parse_gdpr
 * LICENSE: MIT
 *
 * This script parses GDPR text from the webpage into a JSON document
 * It also re-arranges the text into a better version where each individual
 * item in the text is assigned a contextual ID attribute making it
 * easy to reference the particular item.
 */

var FLG_DEBUG = true;
if (!FLG_DEBUG) {
	console.log = function() {};
}

/**
 * @return {jQuery array} returns all GDPR article text
 */
var extract_gdpr_articles_from_page = function() {
    // starting element is the one just before CHAPTER I
    var begin = $('p#d1e1374-1-1').prev();
    // ending element is the div marked final
    var end = $('div.final');
    // first processing element is the one after begin (CHAPTER I)
    var element = begin.next();
    var text = [];

    // continue while we haven't reached the end element
    while (!element.is(end)) {
        text.push(element);
        element = element.next();
    }

    return text;
}
var txt_gdpr = extract_gdpr_articles_from_page();

/**
 * @param  {jQuery array} text contains the text of the GDPR
 * @return {[array of arrays]} chapters extracted from text
 * Each chapter contains the sections and articles within it sequentially
 * in the arrays inside it
 * [chapters] where [chapter] contains everything as jQuery array
 */
var extract_chapters_from_gdpr_text = function(text) {
    var chapters = [];
    var chapter = null;
    var chapter_contents = null;
    for (var i=0; i<text.length; i++) {
        var element = text[i];
        // mark for new chapter
        if(
            // check element type is P
            element.prop('nodeName') == 'P' &&
            // test id syntax
            /^d1e\d+-1-1$/.test(element.prop('id')) && 
            // test text is chapter
            /^\s*CHAPTER [IVX]+\s*$/.test(element.text())
        ) {
            // extract one chapter
        	// the title is in the next element
        	var chapter_title = text[i+1].text().trim();
        	i += 1
        	chapter_contents = [];
			chapter = {
                'number': element.text().trim().slice(8),
                'title': chapter_title,
                "type": "chapter",
                "contents": chapter_contents
            };
            chapters.push(chapter);
        } else {
        	chapter_contents.push(element);
        }
    }
    for(let ch of chapters) {
        // console.log(ch.type, ch.number, ch.contents.length);
    }
    return chapters;
}
var chapters = extract_chapters_from_gdpr_text(txt_gdpr);

/**
 * @param  {[jQuery array]} list contents of chapter
 * @return {[array of arrays]} articles within that chapter
 * Extracts articles from text (chapter)
 */
var extract_articles_from_text = function(text) {
    var articles = [];
    var article = null;
    var article_contents = null;
    for (var i=0; i<text.length; i++) {
        var element = text[i];
        if (
            // if its a P element
            // element.prop('nodeName') == 'P' &&
            // with id of the form
            /^d1e\d+-1-1$/.test(element.prop('id')) &&
            // and text is Article
            /^Article \d+$/.test(element.text())
        ) {
        	var article_title = text[i+1].text().trim();
        	i += 1;
        	article_contents = [];
        	article = {
        		'number': element.text().slice(8),
        		'title': article_title,
        		'type': 'article',
        		'contents': article_contents
        	};
            articles.push(article);
        } else {
        	article_contents.push(element);
        }
    }
    for (let at of articles) {
    	// console.log(at.type, at.number, at.contents.length);
    }

    return articles;
}

/** Article 4 needs special handling
 *	This is because in Article 4, the first point is a generic point without a number,
 *	but the other points are all (weirdly) in a table. Additionally, some of the points
 *	have subpoints as internal tables.
 *
 * The difference between the points in Article 4 and the other articles is the way
 * they are parsed. In Article 4, in addition to each point being a table, the subpoints
 * are embedded in the point itself, whereas in other articles, the subpoints though
 * being a table, are a separate element/item.
 */

/**
 * @param  {[jQuery array]}
 * @return {[map of points]}
 * Each point has the attribute
 * 	- number: digit/null
 * 	- text: text of the point
 * 	- type: text/point
 * 	- subpoints: []
 * 	This function is only to extract points from Article 4
 */
var extract_points_from_article4 = function(article4) {
	var text = article4.contents;
	var points = [];
	var point = null;
	var subpoints = null;
	var subpoint = null;
	for (var i=0; i<text.length; i++) {
		var element = text[i];
		var p_in_element = element.find('p');
		if (p_in_element.length == 0) {
			points.push({
				'number': null,
				'text': element.text().trim(),
				'type': 'text',
				'subpoints': []
			});
			continue;
		}
		var p_number = $(p_in_element[0]);
		var match = p_number.text().match('^\\((\\d+)\\)');
        if (match != undefined && match != null) {
            p_number = match[1];
        } else {
        	p_number = null;
        }
		var p_text = $(p_in_element[1]).text().trim();
		var p_subpoints = p_in_element.slice(2);
		subpoints = [];
		for (var j=0; j<p_subpoints.length; j++) {
			var subpoint_number = $(p_subpoints[j]).text();
			var match = subpoint_number.match('^\\((\\w+)\\)');
			if (match != undefined && match != null) {
	            subpoint_number = match[1];
	        } else {
	        	subpoint_number = null;
	        }
			var subpoint_text = $(p_subpoints[j+1]).text().trim();
			j += 1;
			subpoints.push({
				'number': subpoint_number,
				'text': subpoint_text,
				'type': 'subpoint'
			});
		}
		points.push({
			'number': p_number,
			'text': p_text,
			'type': 'point',
			'subpoints': subpoints
		});
	}
	for(let pt of points) {
		// console.log(pt.type, pt.number, pt.subpoints.length);
		for(let spt of pt.subpoints) {
			// console.log(spt.type, spt.number);
		}
	}

	return points;
}
// var points_in_article4 = extract_points_from_article4(article4);


/**
 * @param  {[jQuery array]} article
 * @return {[map of points]}
 * Each point has the attribute
 * 	- number: digit/null
 * 	- text: text of the point
 * 	- type: text/point
 * 	- subpoints: []
 * Extracts points from article
 */
var extract_points_from_article = function(article) {
    // console.log(article.number);
	var text = article.contents;
	// The extraction mechanism works on the basis of sequential points.
	// This means that if a point has a subpoint,
	// then it will be in the NEXT element as a table

	var points = [];
	var point = null;
	var subpoints = null;
	for(var element of text) {
		var element_type = element.prop('nodeName');
		if (element_type == 'P') {
			var element_text = element.text().trim();
			var match = element_text.match('^(\\d+).');
			if (match == undefined || match == null) {
				// this point has no number
				point = {
					'number': null,
					'text': element_text,
					'type': 'text',
					'subpoints': []
				};
				points.push(point);
			} else {
				// point has a number
				point = {
					'number': match[1],
					'type': 'point',
					'subpoints': []
				};
				point.text = element_text.match('^\\d+.\\s+(.*)')[1];
				points.push(point);
			}
		} else if (element_type == 'TABLE') {
			var p_in_element = element.find('p');
			var p_number = $(p_in_element[0]).text().trim();
			var match = p_number.match('(\\w+)');
			if (match == undefined || match == null) {
				p_number = null;
			} else {
				p_number = match[1];
			}
			var p_text = $(p_in_element[1]).text().trim();
			point.subpoints.push({
				'number': p_number,
				'text': p_text,
				'type': 'subpoint'
			});
		}
	}
	for(pt of points) {
        for(spt of pt.subpoints) {
            // console.log(article.number, pt.number, spt.number);
        }
	}

	return points;
}

/**
 * combine articles in chapter 1 together
 */
var articles_in_chapter_1 = extract_articles_from_text(chapters[0].contents);
var points_in_articles = articles_in_chapter_1.slice(0,3).map(extract_points_from_article);
points_in_articles.push(extract_points_from_article4(articles_in_chapter_1[3]));
for(var i=0; i<articles_in_chapter_1.length; i++) {
	var article = articles_in_chapter_1[i];
	article.contents = points_in_articles[i];
}
chapters[0].contents = articles_in_chapter_1;

/**
 * create the final data object that will hold all the items together
 */
var data = {
    'title': "General Data Protection Regulation",
    'abbrv': "GDPR",
    'regulation': "2016/679",
    'dated': "27/04/2016",
    'updated': "04/05/2016",
    'about': "protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation)",
    'identifier': "L 119/1",
    'language': "EN",
	'chapters': [chapters[0]],
    'recitals': []
};
// chapters yet to be processed
chapters = chapters.slice(1);

/**
 * Process the other chapters
 * Now these other chapters can also contain sections, so the first test to be made
 * is whether a chapter contains any sections. If it does, then the sections get
 * extracted first, and after that the articles need to be extracted from the sections.
 * If a chapter does not contain any sections, then the articles will be extracted
 * directly from the section.
 */

var extract_sections_from_text = function(text) {
	var sections = [];
    var section = null;
    var section_contents = null;
    for (var i=0; i<text.length; i++) {
        var element = text[i];
        if (
            element.prop('nodeName') == 'P' &&
            /^d1e\d+-1-1$/.test(element.prop('id')) &&
            $(element).children('span.expanded').length == 1
        ) {
        	var section_title = text[i+1].text().trim();
        	i += 1;
        	section_contents = [];
        	section = {
        		'number': element.text().trim().slice(7).trim(),
        		'title': section_title,
        		'type': 'section',
        		'contents': section_contents
        	};
            sections.push(section);
        } else {
        	if (section_contents == null) {
        		return null;
        	}
        	section_contents.push(element);
        }
    }
    for (let sec of sections) {
    	// console.log(sec.type, sec.number, sec.contents.length);
    }

    return sections;
}
for(let ch of chapters) {
	var sections = extract_sections_from_text(ch.contents);
	if (sections == null) {
		// console.log(ch.type, ch.number, "does not have Sections");
		var articles = extract_articles_from_text(ch.contents);
		ch.contents = articles;
		for(let at of articles) {
			// console.log(at.type, at.number);
			at.contents = extract_points_from_article(at);
		}
	} else {
		// console.log(ch.type, ch.number, "has Sections");
		ch.contents = sections;
		for(let sec of sections) {
			var articles = extract_articles_from_text(sec.contents);
			for(let at of articles) {
				at.contents = extract_points_from_article(at);
			}
;			sec.contents = articles;
		}
	}
	data.chapters.push(ch);
}

/**
 * DEBUG OUTPUT
 */
// for(let ch of data.chapters) {
// 	console.log(ch.type, ch.number, ch.contents.length);
// 	if (ch.contents[0].type == 'section') {
// 		for(let sec of ch.contents) {
// 			console.log(sec.type, sec.number, sec.contents.length);
// 			for(let at of sec.contents) {
// 				console.log(at.type, at.number, at.contents.length);
// 				for(let pt of at.contents) {
// 					console.log(pt.type, pt.number, pt.subpoints.length);
// 				}
// 			}
// 		}
// 	} else {
// 		for(let at of ch.contents) {
// 			console.log(at.type, at.number, at.contents.length);
// 			for(let pt of at.contents) {
// 				console.log(pt.type, pt.number, pt.subpoints.length);
// 			}
// 		}
// 	}
// }


/**
 * RECITALS
 */
// The recitals start at the table (second) which is after the p element
// with id = d1e40-1-1
var element = $('p#d1e40-1-1');
while(element.prop('nodeName') != 'TABLE') element = element.next();
// At this stage, element points to the table where recitals begin
// Each table holds two p elements, where the first one contains the number
// and the second contains the text 
while(element.prop('nodeName') != 'P') {
    var p_in_element = element.find('p');
    var p_text = $(p_in_element[1]).text().trim();
    var p_number = $(p_in_element[0]).text().match('^\\((\\d+)\\)')[1];
    data.recitals.push({
        'number': p_number,
        'text': p_text,
        'type': 'recital'
    });
    element = element.next();
}

/**
 * CITATIONS
 */
// citations are p elements with class note
data.citations = $('p.note').map(function(index, element) {
    var match = $(element).text().trim().match('^\\((\\d+)\\)\\s+(.*)$')
    return {
        'number': match[1],
        'text': match[2],
        'type': 'citation'
    };
});


/**
 * Download data as JSON
 */
delete data.citations.prevObject;
delete data.citations.context;
delete data.citations.length;
$('<a id="downloadAnchorElem" style="display:none"></a>').appendTo('body');
var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
var btn_download = document.getElementById('downloadAnchorElem');
btn_download.setAttribute("href", dataStr);
btn_download.setAttribute("download", "gdpr.json");
/** TO DOWNLOAD, CALL THIS IN BROWSER CONSOLE **/
// btn_download.click();
