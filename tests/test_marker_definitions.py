from sanity_html import SanityBlockRenderer
from sanity_html.marker_definitions import (
    CommentMarkerDefinition,
    EmphasisMarkerDefinition,
    LinkMarkerDefinition,
    StrikeThroughMarkerDefinition,
    StrongMarkerDefinition,
    UnderlineMarkerDefinition,
)
from sanity_html.types import Block, Span

sample_texts = ['test', None, 1, 2.2, '!"#$%&/()']


def test_render_emphasis_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert EmphasisMarkerDefinition.render(node, 'em', block) == f'<em>{text}</em>'


def test_render_strong_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert StrongMarkerDefinition.render(node, 'strong', block) == f'<strong>{text}</strong>'


def test_render_underline_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert (
            UnderlineMarkerDefinition.render(node, 'u', block)
            == f'<span style="text-decoration:underline;">{text}</span>'
        )


def test_render_strikethrough_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert StrikeThroughMarkerDefinition.render(node, 'strike', block) == f'<del>{text}</del>'


def test_render_link_marker_success():
    for text in sample_texts:
        node = Span(_type='span', marks=['linkId'], text=text)
        block = Block(
            _type='block', children=[node.__dict__], markDefs=[{'_type': 'link', '_key': 'linkId', 'href': text}]
        )
        assert LinkMarkerDefinition.render(node, 'linkId', block) == f'<a href="{text}">{text}</a>'


def test_render_comment_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert CommentMarkerDefinition.render(node, 'comment', block) == f'<!-- {text} -->'


def test_custom_marker_definition():
    from sanity_html.marker_definitions import MarkerDefinition

    class ComicSansEmphasis(MarkerDefinition):
        tag = 'em'

        @classmethod
        def render_prefix(cls, span, marker, context):
            return f'<{cls.tag} style="font-family: "Comic Sans MS", "Comic Sans", cursive;">'

    renderer = SanityBlockRenderer(
        {
            '_type': 'block',
            'children': [{'_key': 'a1ph4', '_type': 'span', 'marks': ['em'], 'text': 'Sanity'}],
            'markDefs': [],
        },
        custom_marker_definitions={'em': ComicSansEmphasis},
    )
    assert renderer.render() == '<p><em style="font-family: "Comic Sans MS", "Comic Sans", cursive;">Sanity</em></p>'
