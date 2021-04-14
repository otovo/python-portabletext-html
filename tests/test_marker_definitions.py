import pytest

from sanity_html.marker_definitions import (
    render_comment_marker,
    render_emphasis_marker,
    render_link_marker,
    render_strong_marker,
)

sample_texts = ['test', None, 1, 2.2, '!"#$%&/()']


def test_render_emphasis_marker_success():
    for text in sample_texts:
        assert render_emphasis_marker(text) == f'<em>{text}</em>'


def test_render_strong_marker_success():
    for text in sample_texts:
        assert render_strong_marker(text) == f'<strong>{text}</strong>'


def test_render_link_marker_success():
    for text in sample_texts:
        assert render_link_marker(text=text, href=text) == f'<a href="{text}">{text}</a>'

    with pytest.raises(TypeError):
        # enforce keyword-only arguments to limit possibility of error
        render_link_marker('test', 'test')


def test_render_comment_marker_success():
    for text in sample_texts:
        assert render_comment_marker(text) == text
