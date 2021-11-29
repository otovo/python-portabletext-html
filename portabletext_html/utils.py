from __future__ import annotations

from typing import TYPE_CHECKING

from portabletext_html.constants import ANNOTATION_MARKER_DEFINITIONS, DECORATOR_MARKER_DEFINITIONS

if TYPE_CHECKING:
    from typing import Type

    from portabletext_html.marker_definitions import MarkerDefinition


def get_default_marker_definitions(mark_defs: list[dict]) -> dict[str, Type[MarkerDefinition]]:
    """
    Convert JSON definitions to a map of marker definition renderers.

    There are two types of markers: decorators and annotations. Decorators are accessed
    by string (`em` or `strong`), while annotations are accessed by a key.
    """
    marker_definitions = {}

    for definition in mark_defs:
        if definition['_type'] in ANNOTATION_MARKER_DEFINITIONS:
            marker = ANNOTATION_MARKER_DEFINITIONS[definition['_type']]
            marker_definitions[definition['_key']] = marker

    return {**marker_definitions, **DECORATOR_MARKER_DEFINITIONS}


def is_list(node: dict) -> bool:
    """Check whether a node is a list node."""
    return 'listItem' in node


def is_span(node: dict) -> bool:
    """Check whether a node is a span node."""
    return node.get('_type', '') == 'span' or isinstance(node, str) or hasattr(node, 'marks')


def is_block(node: dict) -> bool:
    """Check whether a node is a block node."""
    return node.get('_type') == 'block'


def get_list_tags(list_item: str) -> tuple[str, str]:
    """Return the appropriate list tags for a given list item."""
    # TODO: Make it possible for users to pass their own maps, perhaps by adding this to the class
    # and checking optional class context variables defined on initialization.
    return {
        'bullet': ('<ul>', '</ul>'),
        'square': ('<ul style="list-style-type: square">', '</ul>'),
        'number': ('<ol>', '</ol>'),
    }[list_item]
