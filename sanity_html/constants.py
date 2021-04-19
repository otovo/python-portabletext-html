from __future__ import annotations

from typing import TYPE_CHECKING

from sanity_html.marker_serializers import (
    CodeSerializer,
    CommentSerializer,
    EmphasisSerializer,
    LinkSerializer,
    StrikeThroughSerializer,
    StrongSerializer,
    UnderlineSerializer,
)

if TYPE_CHECKING:
    from typing import Dict, Type

    from sanity_html.marker_serializers import MarkerSerializer

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

DECORATOR_MARKER_SERIALIZERS: Dict[str, Type[MarkerSerializer]] = {
    'em': EmphasisSerializer,
    'strong': StrongSerializer,
    'code': CodeSerializer,
    'underline': UnderlineSerializer,
    'strike-through': StrikeThroughSerializer,
}

ANNOTATION_MARKER_SERIALIZERS: Dict[str, Type[MarkerSerializer]] = {
    'link': LinkSerializer,
    'comment': CommentSerializer,
}
