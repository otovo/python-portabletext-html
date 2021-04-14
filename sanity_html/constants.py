from __future__ import annotations

from typing import TYPE_CHECKING

from sanity_html.marker_definitions import (
    CodeMarkerDefinition,
    CommentMarkerDefinition,
    EmphasisMarkerDefinition,
    LinkMarkerDefinition,
    StrongMarkerDefinition,
)

if TYPE_CHECKING:
    from typing import Dict, Type

    from sanity_html.marker_definitions import MarkerDefinition

STYLE_MAP = {
    'h1': 'h1',
    'h2': 'h2',
    'h3': 'h3',
    'h4': 'h4',
    'h5': 'h5',
    'h6': 'h6',
    'normal': 'p',
}

DECORATOR_MARKER_DEFINITIONS: Dict[str, Type[MarkerDefinition]] = {
    'em': EmphasisMarkerDefinition,
    'strong': StrongMarkerDefinition,
    'code': CodeMarkerDefinition,
}

ANNOTATION_MARKER_DEFINITIONS: Dict[str, Type[MarkerDefinition]] = {
    'link': LinkMarkerDefinition,
    'comment': CommentMarkerDefinition,
}
