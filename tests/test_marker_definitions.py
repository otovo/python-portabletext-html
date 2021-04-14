import pytest

from sanity_html.constants import ANNOTATION_MARKER_DEFINITIONS, DECORATOR_MARKER_DEFINITIONS
from sanity_html.marker_definitions import render_comment_marker, render_link_marker

sample_texts = ['test', None, 1, 2.2, '!"#$%&/()']
keys_and_tags = [('em', 'em'), ('strong', 'b'), ('code', 'code'), ('underline', 'u'), ('strike-through', 'strike')]


@pytest.mark.parametrize('key, tag', keys_and_tags)
def test_render_emphasis_marker_success(key, tag):
    """
    Tests all of our decorator mark functions.
    """
    for text in sample_texts:
        assert DECORATOR_MARKER_DEFINITIONS[key](text) == f'<{tag}>{text}</{tag}>'


# Annotation mark tests


def test_render_link_marker_success():
    for text in sample_texts:
        assert render_link_marker(text=text, href=text) == f'<a href="{text}">{text}</a>'

    with pytest.raises(TypeError):
        # enforce keyword-only arguments to limit possibility of error
        ANNOTATION_MARKER_DEFINITIONS['link']('test', 'test')


def test_render_comment_marker_success():
    for text in sample_texts:
        assert render_comment_marker(text) == text
