<a href="https://pypi.org/project/python-sanity-html/">
    <img src="https://img.shields.io/pypi/v/python-sanity-html.svg" alt="Package version">
</a>
<a href="https://codecov.io/gh/otovo/python-sanity-html">
    <img src="https://codecov.io/gh/otovo/python-sanity-html/branch/master/graph/badge.svg" alt="Code coverage">
</a>
<a href="https://pypi.org/project/python-sanity-html/">
    <img src="https://github.com/otovo/python-sanity-html/actions/workflows/test.yml/badge.svg" alt="Test status">
</a>
<a href="https://pypi.org/project/python-sanity-html/">
    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">
</a>
<a href="http://mypy-lang.org/">
    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
</a>

# Python Sanity HTML Renderer

> Repo is currently a work in progress. Not ready to be used.

A python based HTML renderer for [Sanity's](https://www.sanity.io/) [Portable Text](https://github.com/portabletext/portabletext) format.

Written as a python alternative to [Sanity's](https://www.sanity.io/) [block-content-to-html](https://www.npmjs.com/package/%40sanity/block-content-to-html) npm package,
for when you don't have access to a JavaScript runtime.

## Installation

```
pip install python-sanity-html
```

## Usage

To parse your block content as HTML, simply instantiate the parser like this

```python
from sanity_html import SanityBlockRenderer


renderer = SanityBlockRenderer(block_content)
output = renderer.render()
```

## Contributing

Contributions are always appreciated 👏

For details, see the [CONTRIBUTING.md](https://github.com/otovo/python-sanity-html/blob/master/CONTRIBUTING.md). 