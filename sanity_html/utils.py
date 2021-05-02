from __future__ import annotations

from typing import TYPE_CHECKING

from sanity_html.constants import ANNOTATION_MARKER_SERIALIZERS, DECORATOR_MARKER_SERIALIZERS

if TYPE_CHECKING:
    from typing import Type

    from sanity_html.marker_serializers import MarkerSerializer


def get_default_marker_definitions(mark_defs: list[dict]) -> dict[str, Type[MarkerSerializer]]:
    """
    Convert JSON definitions to a map of marker definition renderers.

    There are two types of markers: decorators and annotations. Decorators are accessed
    by string (`em` or `strong`), while annotations are accessed by a key.
    """
    marker_definitions = {}

    for definition in mark_defs:
        if definition['_type'] in ANNOTATION_MARKER_SERIALIZERS:
            marker = ANNOTATION_MARKER_SERIALIZERS[definition['_type']]
            marker_definitions[definition['_key']] = marker

    return {**marker_definitions, **DECORATOR_MARKER_SERIALIZERS}


def is_list(node: dict) -> bool:
    """Check whether a node is a list node."""
    return 'listItem' in node


def is_span(node: dict) -> bool:
    """Check whether a node is a span node."""
    return node.get('_type', '') == 'span' or isinstance(node, str) or hasattr(node, 'marks')


def is_block(node: dict) -> bool:
    """Check whether a node is a block node."""
    return node.get('_type') == 'block'
