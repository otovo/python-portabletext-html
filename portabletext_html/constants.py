from __future__ import annotations

from typing import TYPE_CHECKING

from portabletext_html.marker_definitions import (
    CodeMarkerDefinition,
    CommentMarkerDefinition,
    EmphasisMarkerDefinition,
    LinkMarkerDefinition,
    StrikeThroughMarkerDefinition,
    StrongMarkerDefinition,
    UnderlineMarkerDefinition,
)

if TYPE_CHECKING:
    from typing import Dict, Type

    from portabletext_html.marker_definitions import MarkerDefinition

STYLE_MAP = {
    'h1': 'h1',
    'h2': 'h2',
    'h3': 'h3',
    'h4': 'h4',
    'h5': 'h5',
    'h6': 'h6',
    'blockquote': 'blockquote',
    'normal': 'p',
}

DECORATOR_MARKER_DEFINITIONS: Dict[str, Type[MarkerDefinition]] = {
    'em': EmphasisMarkerDefinition,
    'strong': StrongMarkerDefinition,
    'code': CodeMarkerDefinition,
    'underline': UnderlineMarkerDefinition,
    'strike-through': StrikeThroughMarkerDefinition,
}

ANNOTATION_MARKER_DEFINITIONS: Dict[str, Type[MarkerDefinition]] = {
    'link': LinkMarkerDefinition,
    'comment': CommentMarkerDefinition,
}
