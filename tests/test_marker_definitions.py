from sanity_html.marker_serializers import (
    CommentSerializer,
    EmphasisSerializer,
    LinkSerializer,
    StrikeThroughSerializer,
    StrongSerializer,
    UnderlineSerializer,
)
from sanity_html.types import Block, Span

sample_texts = ['test', None, 1, 2.2, '!"#$%&/()']


def test_render_emphasis_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert EmphasisSerializer.render(node, 'em', block) == f'<em>{text}</em>'


def test_render_strong_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert StrongSerializer.render(node, 'strong', block) == f'<strong>{text}</strong>'


def test_render_underline_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert UnderlineSerializer.render(node, 'u', block) == f'<span style="text-decoration:underline;">{text}</span>'


def test_render_strikethrough_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert StrikeThroughSerializer.render(node, 'strike', block) == f'<del>{text}</del>'


def test_render_link_marker_success():
    for text in sample_texts:
        node = Span(_type='span', marks=['linkId'], text=text)
        block = Block(
            _type='block', children=[node.__dict__], markDefs=[{'_type': 'link', '_key': 'linkId', 'href': text}]
        )
        assert LinkSerializer.render(node, 'linkId', block) == f'<a href="{text}">{text}</a>'


def test_render_comment_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert CommentSerializer.render(node, 'comment', block) == f'<!-- {text} -->'
