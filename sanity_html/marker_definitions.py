from __future__ import annotations

from typing import TYPE_CHECKING

# Decorators


if TYPE_CHECKING:
    from typing import Type

    from sanity_html.dataclasses import Block, Span


class MarkerDefinition:
    """Base class for marker definition handlers."""

    tag: str

    @classmethod
    def render_prefix(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
        """Render the prefix for the marked span.

        Usually this this the opening of the HTML tag.
        """
        return f'<{cls.tag}>'

    @classmethod
    def render_suffix(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
        """Render the suffix for the marked span.

        Usually this this the closing of the HTML tag.
        """
        return f'</{cls.tag}>'

    @classmethod
    def render(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
        """Render the marked span directly with prefix and suffix."""
        result = cls.render_prefix(span, marker, context)
        result += str(span.text)
        result += cls.render_suffix(span, marker, context)
        return result


class EmphasisMarkerDefinition(MarkerDefinition):
    """Marker definition for <em> rendering."""

    tag = 'em'


class StrongMarkerDefinition(MarkerDefinition):
    """Marker definition for <strong> rendering."""

    tag = 'strong'


class CodeMarkerDefinition(MarkerDefinition):
    """Marker definition for <code> rendering."""

    tag = 'code'


# Annotations


class LinkMarkerDefinition(MarkerDefinition):
    """Marker definition for link rendering."""

    tag = 'a'

    @classmethod
    def render_prefix(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
        """Render the opening anchor tag with the href attribute set.

        The href attribute is fetched from the provided block context using
        the provided marker key.
        """
        marker_defintion = next((md for md in context.markDefs if md['_key'] == marker), None)
        if not marker_defintion:
            raise ValueError(f'Marker definition for key: {marker} not found in parent block context')
        href = marker_defintion['href']
        return f'<a href="{href}">'


class CommentMarkerDefinition(MarkerDefinition):
    """Marker definition for HTML comment rendering."""

    tag = '!--'

    @classmethod
    def render_prefix(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
        """Render the opening of the HTML comment block."""
        return '<!-- '

    @classmethod
    def render_suffix(cls: Type[MarkerDefinition], span: Span, marker: str, context: Block) -> str:
        """Render the closing part of the HTML comment block."""
        return ' -->'
