Tolerant JSONDecoder
====================

Description
-----------
This extends the Python default json parser to parse JSON documents with 
single-quote delimited strings, which is outside the standard of JSON.

Motivation
----------
When scraping webpages, occasionally it can be useful to extract some of the 
JavaScript datastructures.

It is problematic to parse this content, without using a Javascript parser
such as `pyjsparser https://github.com/PiotrDabkowski/pyjsparser` or 
`esprima-python https://github.com/Kronuz/esprima-python`

This is still suboptimal, as taking that approach still leaves you with a syntax 
tree that you need to convert into Python objects, assuming this is your end 
goal.

The Python JSON library is great - one can also do easy things like find the 
start of a data-structure, then use jason.JSONDecoder().raw_decode() and it
will work out where the data-structure ends, which saves on trying to identify
the end of any data-structure yourself.

Unfortunately, when trying to decode these data-structures, one discovers that
they can be valid JavaScript, but they are not strict JSON, which allows only
double-quoted strings to appear in its data-structures.

Some of the advice around suggests using ast.literal_eval(), however this fails
when boolean constants are present, as :code:`true` and :code:`false` not parseable 
tokens in Python, e.g. :code:`["asdf", 'asdf", false]` will not parse using this 
approach.

Therefore, to fix the problem, I've written a custom JSONDecoder which is 
tolerant of single quoted strings.  This is a small monkey-patch of the default 
JSONDecoder.

Usage
-----

The decoder may be used as follows:

.. code-block:: python

    import json
    import tolerantjsondecoder

    jsonText = """{'a':"b", "c":'d'}"""
    data = json.loads(jsonText, cls = tolerantjsondecoder.JSONDecoder)
    print(data)

or, alternatively:

.. code-block:: python

    import tolerantjsondecoder

    jsonDecoder = tolerantjsondecoder.JSONDecoder()

    htmlDoc = """
    <html>
    <body>
    <script>
    var cheeseCollection=['cheddar', 'camembert', 'roquefort']
    </script>
    </body>
    </hmtl>
    """

    startTag = 'var cheeseCollection='
    idx = htmlDoc.find(startTag) + len(startTag)
    cheeses = jsonDecoder.raw_decode(htmlDoc[idx:])
    print(cheeses)[0]
