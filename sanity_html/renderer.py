from __future__ import annotations

import html
from collections import deque
from typing import TYPE_CHECKING

from sanity_html.constants import STYLE_MAP
from sanity_html.marker_serializers import DefaultMarkerSerializer
from sanity_html.serializers.lists import ListSerializer
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

        self._list_serializer = ListSerializer(self)

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
        list_item: bool = False,
        child_idx: Optional[int] = None,
    ) -> str:
        """
        Call the correct render method depending on the node type.

        :param node: Block content node - can be block, span, or list (block).
        :param context: Optional context. Spans are passed with a Block instance as context for mark lookups.
        :param list_item: Whether we are handling a list upstream (impacts block handling).
        :param child_idx: 0-based index of this node in the parent node children array.
        """
        if is_list(node):
            serializer = ListSerializer(self)
            return serializer.render(node, blocks)
        elif is_block(node):
            block = Block(**node, marker_definitions=self._custom_marker_definitions)
            return self._render_block(block, list_item=list_item)

        elif is_span(node):
            if isinstance(node, str):
                # TODO: Remove if we there's no coverage for this after we've fixed tests
                #  not convinced this code path is possible - put it in because the sanity lib checks for it
                span = Span(**{'text': node})
            else:
                span = Span(**node)

            assert context  # this should be a cast
            return self._render_span(span, block=context, child_idx=child_idx)  # context is span's outer block
        elif self._custom_serializers.get(node.get('_type', '')):
            return self._custom_serializers.get(node.get('_type', ''))(node, context, list_item)  # type: ignore
        else:
            print('Unexpected code path 👺')  # noqa: T001 # TODO: Remove after thorough testing
            return ''

    def _render_block(self, block: Block, list_item: bool = False) -> str:
        text, tag = '', STYLE_MAP[block.style]

        if not list_item or tag != 'p':
            text += f'<{tag}>'

        children = deque(block.children)
        for idx, child_node in enumerate(block.children):
            text += self._render_node(children, child_node, context=block, child_idx=idx)

        if not list_item or tag != 'p':
            text += f'</{tag}>'

        return text

    def _render_span(self, span: Span, block: Block, child_idx: Optional[int] = None) -> str:
        result: str = ''
        prev_node, next_node = block.get_node_siblings(span, child_idx=child_idx)
        prev_marks = prev_node.get('marks', []) if prev_node else []
        next_marks = next_node.get('marks', []) if next_node else []

        sorted_marks = sorted(span.marks, key=lambda x: -block.marker_frequencies[x])
        for mark in sorted_marks:
            if mark in prev_marks:
                continue
            marker_callable = block.marker_definitions.get(mark, DefaultMarkerSerializer)()
            result += marker_callable.render_prefix(span, mark, block)

        result += html.escape(span.text).replace('\n', '<br/>')

        for mark in reversed(sorted_marks):
            if mark in next_marks:
                continue

            marker_callable = block.marker_definitions.get(mark, DefaultMarkerSerializer)()
            result += marker_callable.render_suffix(span, mark, block)

        return result


def render(blocks: List[Dict], *args, **kwargs) -> str:
    """Shortcut function inspired by Sanity's own blocksToHtml.h callable."""
    renderer = SanityBlockRenderer(blocks, *args, **kwargs)
    return renderer.render()
