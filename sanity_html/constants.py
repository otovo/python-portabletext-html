from __future__ import annotations

from typing import TYPE_CHECKING

from sanity_html.marker_definitions import generate_decorator_marker_callable, render_comment_marker, render_link_marker

if TYPE_CHECKING:
    from typing import Callable, Dict

STYLE_MAP = {
    'h1': 'h1',
    'h2': 'h2',
    'h3': 'h3',
    'h4': 'h4',
    'h5': 'h5',
    'h6': 'h6',
    'normal': 'p',
}

DECORATOR_MARKER_DEFINITIONS: Dict[str, Callable] = {
    'em': generate_decorator_marker_callable('em'),
    'strong': generate_decorator_marker_callable('b'),
    'code': generate_decorator_marker_callable('code'),
    'underline': generate_decorator_marker_callable('u'),
    'strike-through': generate_decorator_marker_callable('strike'),
}

ANNOTATION_MARKER_DEFINITIONS: Dict[str, Callable] = {
    'link': render_link_marker,
    'comment': render_comment_marker,
}
