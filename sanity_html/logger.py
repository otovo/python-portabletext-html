"""
Logging setup.

The rest of the code gets the logger through this module rather than
`logging.getLogger` to make sure that it is configured.
"""
import logging

logger = logging.getLogger('sanity_html')

if not logger.handlers:  # pragma: no cover
    logger.setLevel(logging.WARNING)
    logger.addHandler(logging.NullHandler())
