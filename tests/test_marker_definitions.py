from sanity_html.dataclasses import Block, Span
from sanity_html.marker_definitions import (
    CommentMarkerDefinition,
    EmphasisMarkerDefinition,
    LinkMarkerDefinition,
    StrongMarkerDefinition,
)

sample_texts = ['test', None, 1, 2.2, '!"#$%&/()']


def test_render_emphasis_marker_success():
    for text in sample_texts:
        node = Span(**{'_type': 'span', 'text': text})
        block = Block(_type='block', children=[node])
        assert EmphasisMarkerDefinition.render(node, 'em', block) == f'<em>{text}</em>'


def test_render_strong_marker_success():
    for text in sample_texts:
        node = Span(**{'_type': 'span', 'text': text})
        block = Block(_type='block', children=[node])
        assert StrongMarkerDefinition.render(node, 'strong', block) == f'<strong>{text}</strong>'


def test_render_link_marker_success():
    for text in sample_texts:
        node = Span(**{'_type': 'span', 'marks': ['linkId'], 'text': text})
        block = Block(_type='block', children=[node], markDefs=[{'_type': 'link', '_key': 'linkId', 'href': text}])
        assert LinkMarkerDefinition.render(node, 'linkId', block) == f'<a href="{text}">{text}</a>'


def test_render_comment_marker_success():
    for text in sample_texts:
        node = Span(**{'_type': 'span', 'text': text})
        block = Block(_type='block', children=[node])
        assert CommentMarkerDefinition.render(node, 'comment', block) == f'<!-- {text} -->'
