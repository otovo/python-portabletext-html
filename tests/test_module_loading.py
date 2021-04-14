"""Smoke tests for the library."""


def test_module_should_be_importable():
    """Test that we can load the module.

    This catches any compilation issue we might have.
    """
    from sanity_html import SanityBlockRenderer

    assert SanityBlockRenderer
