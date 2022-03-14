# pylint: skip-file
from typing import Type

from portabletext_html import PortableTextRenderer
from portabletext_html.marker_definitions import (
    CommentMarkerDefinition,
    EmphasisMarkerDefinition,
    LinkMarkerDefinition,
    StrikeThroughMarkerDefinition,
    StrongMarkerDefinition,
    UnderlineMarkerDefinition,
)
from portabletext_html.types import Block, Span

sample_texts = ['test', None, 1, 2.2, '!"#$%&/()']


def test_render_emphasis_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert EmphasisMarkerDefinition.render_text(node, 'em', block) == f'{text}'
        assert EmphasisMarkerDefinition.render(node, 'em', block) == f'<em>{text}</em>'


def test_render_strong_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert StrongMarkerDefinition.render_text(node, 'strong', block) == f'{text}'
        assert StrongMarkerDefinition.render(node, 'strong', block) == f'<strong>{text}</strong>'


def test_render_underline_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert UnderlineMarkerDefinition.render_text(node, 'u', block) == f'{text}'
        assert (
            UnderlineMarkerDefinition.render(node, 'u', block)
            == f'<span style="text-decoration:underline;">{text}</span>'
        )


def test_render_strikethrough_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert StrikeThroughMarkerDefinition.render_text(node, 'strike', block) == f'{text}'
        assert StrikeThroughMarkerDefinition.render(node, 'strike', block) == f'<del>{text}</del>'


def test_render_link_marker_success():
    for text in sample_texts:
        node = Span(_type='span', marks=['linkId'], text=text)
        block = Block(
            _type='block', children=[node.__dict__], markDefs=[{'_type': 'link', '_key': 'linkId', 'href': text}]
        )
        assert LinkMarkerDefinition.render_text(node, 'linkId', block) == f'{text}'
        assert LinkMarkerDefinition.render(node, 'linkId', block) == f'<a href="{text}">{text}</a>'


def test_render_comment_marker_success():
    for text in sample_texts:
        node = Span(_type='span', text=text)
        block = Block(_type='block', children=[node.__dict__])
        assert CommentMarkerDefinition.render(node, 'comment', block) == f'<!-- {text} -->'


def test_custom_marker_definition():
    from portabletext_html.marker_definitions import MarkerDefinition

    class ConditionalMarkerDefinition(MarkerDefinition):
        tag = 'em'

        @classmethod
        def render_prefix(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
            marker_definition = next((md for md in context.markDefs if md['_key'] == marker), None)
            condition = marker_definition.get('cloudCondition', '')
            if not condition:
                style = 'display: none'
                return f'<{cls.tag} style=\"{style}\">'
            else:
                return super().render_prefix(span, marker, context)

        @classmethod
        def render_text(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
            marker_definition = next((md for md in context.markDefs if md['_key'] == marker), None)
            condition = marker_definition.get('cloudCondition', '')
            return span.text if not condition else ''

    renderer = PortableTextRenderer(
        blocks={
            '_type': 'block',
            'children': [{'_key': 'a1ph4', '_type': 'span', 'marks': ['some_id'], 'text': 'Sanity'}],
            'markDefs': [{'_key': 'some_id', '_type': 'contractConditional', 'cloudCondition': False}],
        },
        custom_marker_definitions={'contractConditional': ConditionalMarkerDefinition},
    )
    result = renderer.render()
    assert result == '<p><em style="display: none">Sanity</em></p>'
