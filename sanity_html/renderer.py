from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from sanity_html.constants import STYLE_MAP
from sanity_html.serializers.lists import ListSerializer
from sanity_html.serializers.spans import SpanSerializer
from sanity_html.types import Block, Span
from sanity_html.utils import is_block, is_list, is_span

if TYPE_CHECKING:
    from typing import Callable, Dict, List, Optional, Type, Union

    from sanity_html.marker_serializers import MarkerSerializer


class SanityBlockRenderer:
    """HTML renderer for Sanity block content."""

    def __init__(
        self,
        blocks: Union[list[dict], dict],
        custom_marker_definitions: dict[str, Type[MarkerSerializer]] = None,
        custom_serializers: dict[str, Callable[[dict, Optional[Block], bool], str]] = None,
    ) -> None:
        self._wrapper_element: Optional[str] = None
        self._custom_marker_definitions = custom_marker_definitions or {}
        self._custom_serializers = custom_serializers or {}

        if isinstance(blocks, dict):
            self._blocks = [blocks]
        elif isinstance(blocks, list):
            self._blocks = blocks
            self._wrapper_element = 'div' if len(blocks) > 1 else ''

    def render(self) -> str:
        """Render HTML from self._blocks."""
        if not self._blocks:
            return ''

        result = ''
        blocks = deque(self._blocks)
        while blocks:
            node = blocks.popleft()
            result += self._render_node(blocks, node)  # render non-list nodes immediately

        result = result.strip()

        if self._wrapper_element:
            return f'<{self._wrapper_element}>{result}</{self._wrapper_element}>'
        return result

    def _render_node(
        self,
        blocks: deque[dict],
        node: dict,
        context: Optional[Block] = None,
        inline: bool = False,
        child_idx: Optional[int] = None,
    ) -> str:
        """
        Call the correct render method depending on the node type.

        :param node: Block content node - can be block, span, or list (block).
        :param context: Optional context. Spans are passed with a Block instance as context for mark lookups.
        :param inline: Whether the node should be wrapped.
        :param child_idx: 0-based index of this node in the parent node children array.
        """
        if is_list(node):
            return ListSerializer(self)(node, blocks)
        elif is_block(node):
            block = Block(**node, marker_definitions=self._custom_marker_definitions)
            return self._render_block(block, inline=inline)
        elif is_span(node):
            assert context  # this should be a cast
            return SpanSerializer(self)(node, context, child_idx)
        elif self._custom_serializers.get(node.get('_type', '')):
            return self._custom_serializers.get(node.get('_type', ''))(node, context, inline)  # type: ignore
        else:
            print('Unexpected code path 👺')  # noqa: T001 # TODO: Remove after thorough testing
            return ''

    def _render_block(self, block: Block, inline: bool = False) -> str:
        text, tag = '', STYLE_MAP[block.style]

        if not inline or tag != 'p':
            text += f'<{tag}>'

        children = deque(block.children)
        for idx, child_node in enumerate(block.children):
            text += self._render_node(children, child_node, context=block, child_idx=idx)

        if not inline or tag != 'p':
            text += f'</{tag}>'

        return text


def render(blocks: List[Dict], *args, **kwargs) -> str:
    """Shortcut function inspired by Sanity's own blocksToHtml.h callable."""
    renderer = SanityBlockRenderer(blocks, *args, **kwargs)
    return renderer.render()
