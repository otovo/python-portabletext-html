from __future__ import annotations

from typing import TYPE_CHECKING

from sanity_html.marker_definitions import (
    render_comment_marker,
    render_emphasis_marker,
    render_link_marker,
    render_strong_marker,
)

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
    'em': render_emphasis_marker,
    'strong': render_strong_marker,
}

ANNOTATION_MARKER_DEFINITIONS: Dict[str, Callable] = {
    'link': render_link_marker,
    'comment': render_comment_marker,
}
