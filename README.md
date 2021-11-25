<a href="https://pypi.org/project/sanity-html/">
    <img src="https://img.shields.io/pypi/v/sanity-html.svg" alt="Package version">
</a>
<a href="https://codecov.io/gh/otovo/python-sanity-html">
    <img src="https://codecov.io/gh/otovo/python-sanity-html/branch/main/graph/badge.svg" alt="Code coverage">
</a>
<a href="https://pypi.org/project/python-sanity-html/">
    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">
</a>
<a href="http://mypy-lang.org/">
    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
</a>

# Sanity HTML Renderer for Python

This package generates HTML from [Portable Text](https://github.com/portabletext/portabletext).

For the most part, it mirrors [Sanity's](https://www.sanity.io/) own [block-content-to-html](https://www.npmjs.com/package/%40sanity/block-content-to-html) NPM library.

## Installation

```
pip install sanity-html
```

## Usage

Instantiate the `SanityBlockRenderer` class with your content and call the `render` method.

The following content

```python
from sanity_html import SanityBlockRenderer

renderer = SanityBlockRenderer({
    "_key": "R5FvMrjo",
    "_type": "block",
    "children": [
        {"_key": "cZUQGmh4", "_type": "span", "marks": ["strong"], "text": "A word of"},
        {"_key": "toaiCqIK", "_type": "span", "marks": ["strong"], "text": " warning;"},
        {"_key": "gaZingsA", "_type": "span", "marks": [], "text": " Sanity is addictive."}
    ],
    "markDefs": [],
    "style": "normal"
})
renderer.render()
```

Generates this HTML
```html
<p><strong>A word of warning;</strong> Sanity is addictive.</p>
```

### Supported types

The `block` and `span` types are supported out of the box.

### Custom types

Beyond the built-in types, you have the freedom to provide
your own serializers to render any custom `_type` the way you
would like to.

To illustrate, if you passed this data to the renderer class:

```python
from sanity_html import SanityBlockRenderer

renderer = SanityBlockRenderer({
  "_type": "block",
  "_key": "foo",
  "style": "normal",
  "children": [
    {
      "_type": "span",
      "text": "Press, "
    },
    {
      "_type": "button",
      "text": "here"
    },
    {
      "_type": "span",
      "text": ", now!"
    }
  ]
})
renderer.render()
```

The renderer would actually throw an error here, since `button`
does not have a corresponding built-in type serializer by default.

To render this text you must provide your own serializer, like this:

```python
from sanity_html import SanityBlockRenderer

def button_serializer(node: dict, context: Optional[Block], list_item: bool):
    return f'<button>{node["text"]}</button>'

renderer = SanityBlockRenderer(
    ...,
    custom_serializers={'button': button_serializer}
)
output = renderer.render()
```

With the custom serializer provided, the renderer would now successfully
output the following HTML:

```html
<p>Press <button>here</button>, now!</p>
```

### Supported mark definitions

The package provides several built-in marker definitions and styles:

**decorator marker definitions**

- `em`
- `strong`
- `code`
- `underline`
- `strike-through`

**annotation marker definitions**

- `link`
- `comment`

### Custom mark definitions

Like with custom type serializers, additional serializers for
marker definitions and styles can be passed in like this:

```python
from sanity_html import SanityBlockRenderer

renderer = SanityBlockRenderer(
    ...,
    custom_marker_definitions={'em': ComicSansEmphasis}
)
renderer.render()
```

The primary difference between a type serializer and a mark definition serializer
is that the latter uses a class structure, and has three required methods.

Here's an example of a custom style, adding an extra font
to the built-in equivalent serializer:

```python
from sanity_html.marker_definitions import MarkerDefinition


class ComicSansEmphasis(MarkerDefinition):
    tag = 'em'

    @classmethod
    def render_prefix(cls, span: Span, marker: str, context: Block) -> str:
        return f'<{cls.tag} style="font-family: "Comic Sans MS", "Comic Sans", cursive;">'

    @classmethod
    def render_suffix(cls, span: Span, marker: str, context: Block) -> str:
        return f'</{cls.tag}>'

    @classmethod
    def render(cls, span: Span, marker: str, context: Block) -> str:
        result = cls.render_prefix(span, marker, context)
        result += str(span.text)
        result += cls.render_suffix(span, marker, context)
        return result
```

Since the `render_suffix` and `render` methods here are actually identical to the base class,
they do not need to be specified, and the whole example can be reduced to:

```python
from sanity_html.marker_definitions import MarkerDefinition  # base
from sanity_html import SanityBlockRenderer

class ComicSansEmphasis(MarkerDefinition):
    tag = 'em'

    @classmethod
    def render_prefix(cls, span: Span, marker: str, context: Block) -> str:
        return f'<{cls.tag} style="font-family: "Comic Sans MS", "Comic Sans", cursive;">'


renderer = SanityBlockRenderer(
    ...,
    custom_marker_definitions={'em': ComicSansEmphasis}
)
renderer.render()
```


### Supported styles

Blocks can optionally define a `style` tag. These styles are supported:

- `h1`
- `h2`
- `h3`
- `h4`
- `h5`
- `h6`
- `blockquote`
- `normal`

## Missing features

For anyone interested, we would be happy to see a
default built-in serializer for the `image` type added.
In the meantime, users should be able to serialize image types by passing a custom serializer.

## Contributing

Contributions are always appreciated 👏

For details, see the [CONTRIBUTING.md](https://github.com/otovo/python-sanity-html/blob/main/CONTRIBUTING.md).
