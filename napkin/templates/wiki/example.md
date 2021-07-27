[TOC]


# Text

It's very easy to make some words **bold** and other 
words *italic* with Markdown. You can 
even [link to Google!](http://google.com)

* * *

# Lists

Sometimes you want numbered lists:

1. One
2. Two
3. Three

Sometimes you want bullet points:

* Start a line with a star
* Profit!

Alternatively,

- Dashes work just as well
- And if you have sub points, put two spaces before the dash or star:
  - Like this
  - And this


#  Images

If you want to embed images, this is how you do it:

![Image of Huron](http://hihuron.com/image/logo_1.png)


# Headers & Quotes

# Structured documents

Sometimes it's useful to have different levels of headings to structure your documents. Start lines with a `#` to create headings. Multiple `##` in a row denote smaller heading sizes.

### This is a third-tier heading

You can use one `#` all the way up to `######` six for different heading sizes.

***

If you'd like to quote someone, use the > character before the line:

> Coffee. The finest organic suspension ever devised... I beat the Borg with it.
> - Captain Janeway


# Code

There are many different ways to style code with GitHub's markdown. If you have inline code blocks, wrap them in backticks: `var example = true`.  If you've got a longer block of code, you can indent with four spaces:

    if (isAwesome){
      return true
    }

GitHub also supports something called code fencing, which allows for multiple lines without indentation:

```
if (isAwesome){
  return true
}
```

And if you'd like to use syntax highlighting, include the language:

```javascript
if (isAwesome){
  return true
}
```


* * *

```python
def hello(world):
    print world
```

***

```
def hello(world):
    print world
```
{: #code1 .codehilite .language-python }


* * *


# Extras

GitHub supports many extras in Markdown that help you reference and link to people. If you ever want to direct a comment at someone, you can prefix their name with an @ symbol: Hey @kneath - love your sweater!

But I have to admit, tasks lists are my favorite:

- [x] This is a complete item
- [ ] This is an incomplete item

When you include a task list in the first comment of an Issue, you will see a helpful progress bar in your list of issues. It works in Pull Requests, too!

And, of course emoji! :sparkles: :camel: :boom:


* * *


# Extensions


## Extra

### Markdown Inside HTML Blocks

This is *true* markdown text.

<div markdown="1">
This is *true* markdown text.
</div>


### Abbreviations

The HTML specification 
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium


### Attribute Lists


A setext style header {: #setext .btn-primary}
=================================

### A hash style header ### {: #hash .btn-blue }

To define attributes for a block level element, the attribute list should be defined on the last line of the block by itself.

*[link](http://example.com){: class="btn-warning" title="Some title!" }*


A word which starts with a `hash (#)` will set the id of an element.
A word which starts with a `dot (.)` will be added to the list of classes assigned to an element.
A key/value pair (somekey='some value') will assign that pair to the element.
Be aware that while the `dot syntax` will add to a class, using key/value pairs will always override the previously defined attribute. Consider the following:
{: #an_id .btn-red }


### Definition Lists

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.


### Fenced Code Blocks

This is a paragraph introducing:

~~~~~~~~~~~~~~~~~~~~
a one-line code block
~~~~~~~~~~~~~~~~~~~~



~~~~{.python}
# python code
~~~~

~~~~.html
<p>HTML Document</p>
~~~~


```python
# more python code
def flask_request_args_get_others(req, excluding=[]):
    args = flask_req_get_querystr(req)
    r = {}
    for k, v in args.items():
        if k and v and k not in excluding:
            r[k] = v
    return r

```

~~~~{.python hl_lines="1 3"}
# This line is emphasized
# This line isn't
# This line is emphasized
~~~~

… or with GitHub’s:

```python hl_lines="1 3"
# This line is emphasized
# This line isn't
# This line is emphasized
```


### Footnotes

Python-Markdown’s Footnote syntax follows the generally accepted syntax of the Markdown community at large and almost exactly matches PHP Markdown Extra‘s implementation of footnotes. The only differences involve a few subtleties in the output.

Example:

Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".


### Tables

First Header | Second Header
------------ | -------------
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column{: .table }



## Admonition

The Admonition extension adds rST-style admonitions to Markdown documents.

This extension is included in the standard Markdown library.

!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.

!!! note
    You should note that the title will be automatically capitalized.

!!! danger "Don't try this at home"
    Optionally, you can use custom titles. For instance:

!!! important ""
    This is a admonition box without a title.





