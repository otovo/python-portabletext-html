from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


# Decorators


def generate_decorator_marker_callable(tag: str) -> Callable:
    """Return a callable."""

    def inner(text: str) -> str:
        return f'<{tag}>{text}</{tag}>'

    return inner


# Annotations


def render_link_marker(*, text: str, href: str) -> str:
    """Add link tags."""
    return f'<a href="{href}">{text}</a>'


def render_comment_marker(text: str) -> str:
    """Add comment tags."""
    return text  # TODO: Remove or refine - comment markers are briefly mentioned in the portable text spec
