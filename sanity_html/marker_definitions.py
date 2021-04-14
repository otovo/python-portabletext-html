# Decorators


def render_emphasis_marker(text: str) -> str:
    """Add emphasis tags."""
    return f'<em>{text}</em>'


def render_strong_marker(text: str) -> str:
    """Add strong tags."""
    return f'<strong>{text}</strong>'


# Annotations


def render_link_marker(*, text: str, href: str) -> str:
    """Add link tags."""
    return f'<a href="{href}">{text}</a>'


def render_comment_marker(text: str) -> str:
    """Add comment tags."""
    return text  # TODO: Remove or refine - comment markers are briefly mentioned in the portable text spec
