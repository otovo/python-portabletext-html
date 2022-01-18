from __future__ import annotations

import html
from typing import TYPE_CHECKING, cast

from portabletext_html.constants import STYLE_MAP
from portabletext_html.logger import logger
from portabletext_html.marker_definitions import DefaultMarkerDefinition
from portabletext_html.types import Block, Span
from portabletext_html.utils import get_list_tags, is_block, is_list, is_span

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Type, Union

    from portabletext_html.marker_definitions import MarkerDefinition


class UnhandledNodeError(Exception):
    """Raised when we receive a node that we cannot parse."""

    pass


class MissingSerializerError(UnhandledNodeError):
    """
    Raised when an unrecognized node _type value is found.

    This usually means that you need to pass a custom serializer
    to handle the custom type.
    """

    pass


class PortableTextRenderer:
    """HTML renderer for Sanity's portable text format."""

    def __init__(
        self,
        blocks: Union[list[dict], dict],
        custom_marker_definitions: dict[str, Type[MarkerDefinition]] = None,
        custom_serializers: dict[str, Callable[[dict, Optional[Block], bool], str]] = None,
    ) -> None:
        logger.debug('Initializing block renderer')
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
        logger.debug('Rendering HTML')

        if not self._blocks:
            return ''

        result = ''
        list_nodes: List[Dict] = []

        for node in self._blocks:

            if list_nodes and not is_list(node):
                tree = self._normalize_list_tree(list_nodes)
                result += ''.join([self._render_node(n, Block(**node), list_item=True) for n in tree])
                list_nodes = []  # reset list_nodes

            if is_list(node):
                list_nodes.append(node)
                continue  # handle all elements ^ when the list ends

            result += self._render_node(node)  # render non-list nodes immediately

        if list_nodes:
            tree = self._normalize_list_tree(list_nodes)
            result += ''.join(self._render_node(n, Block(**node), list_item=True) for n in tree)

        result = result.strip()

        if self._wrapper_element:
            return f'<{self._wrapper_element}>{result}</{self._wrapper_element}>'
        return result

    def _render_node(self, node: dict, context: Optional[Block] = None, list_item: bool = False) -> str:
        """
        Call the correct render method depending on the node type.

        :param node: Block content node - can be block, span, or list (block).
        :param context: Optional context. Spans are passed with a Block instance as context for mark lookups.
        :param list_item: Whether we are handling a list upstream (impacts block handling).
        """
        if is_list(node):
            logger.debug('Rendering node as list')
            block = Block(**node, marker_definitions=self._custom_marker_definitions)
            return self._render_list(block, context)

        elif is_block(node):
            logger.debug('Rendering node as block')
            block = Block(**node, marker_definitions=self._custom_marker_definitions)
            return self._render_block(block, list_item=list_item)

        elif is_span(node):
            logger.debug('Rendering node as span')
            span = Span(**node)
            context = cast(Block, context)  # context should always be a Block here
            return self._render_span(span, block=context)

        elif self._custom_serializers.get(node.get('_type', '')):
            return self._custom_serializers.get(node.get('_type', ''))(node, context, list_item)  # type: ignore

        else:
            if hasattr(node, '_type'):
                raise MissingSerializerError(
                    f'Found unhandled node type: {node["_type"]}. ' 'Most likely this requires a custom serializer.'
                )
            else:
                raise UnhandledNodeError(f'Received node that we cannot handle: {node}')

    def _render_block(self, block: Block, list_item: bool = False) -> str:
        text, tag = '', STYLE_MAP[block.style]

        if not list_item or tag != 'p':
            text += f'<{tag}>'

        for child_node in block.children:
            text += self._render_node(child_node, context=block)

        if not list_item or tag != 'p':
            text += f'</{tag}>'

        return text

    def _render_span(self, span: Span, block: Block) -> str:
        logger.debug('Rendering span')
        result: str = ''
        prev_node, next_node = block.get_node_siblings(span)

        prev_marks = prev_node.get('marks', []) if prev_node else []
        next_marks = next_node.get('marks', []) if next_node else []

        sorted_marks = sorted(span.marks, key=lambda x: -block.marker_frequencies[x])
        for mark in sorted_marks:
            if mark in prev_marks:
                continue

            marker_callable = block.marker_definitions.get(mark, DefaultMarkerDefinition)()
            result += marker_callable.render_prefix(span, mark, block)

        result += html.escape(span.text).replace('\n', '<br/>')

        for mark in reversed(sorted_marks):
            if mark in next_marks:
                continue

            marker_callable = block.marker_definitions.get(mark, DefaultMarkerDefinition)()
            result += marker_callable.render_suffix(span, mark, block)

        return result

    def _render_list(self, node: Block, context: Optional[Block]) -> str:
        assert node.listItem
        head, tail = get_list_tags(node.listItem)
        result = head
        for child in node.children:
            result += f'<li>{self._render_block(Block(**child), True)}</li>'
        result += tail
        return result

    def _normalize_list_tree(self, nodes: list) -> list[dict]:
        tree = []

        current_list = None
        for node in nodes:
            if not is_block(node):
                tree.append(node)
                current_list = None
                continue

            if current_list is None:
                current_list = self._list_from_block(node)
                tree.append(current_list)
                continue

            if node.get('level') == current_list['level'] and node.get('listItem') == current_list['listItem']:
                current_list['children'].append(node)
                continue

            if node.get('level') > current_list['level']:
                new_list = self._list_from_block(node)
                current_list['children'][-1]['children'].append(new_list)
                current_list = new_list
                continue

            if node.get('level') < current_list['level']:
                parent = self._find_list(tree[-1], level=node.get('level'), list_item=node.get('listItem'))
                if parent:
                    current_list = parent
                    current_list['children'].append(node)
                    continue
                current_list = self._list_from_block(node)
                tree.append(current_list)
                continue

            if node.get('listItem') != current_list['listItem']:
                match = self._find_list(tree[-1], level=node.get('level'))
                if match and match['listItem'] == node.get('listItem'):
                    current_list = match
                    current_list['children'].append(node)
                    continue
                current_list = self._list_from_block(node)
                tree.append(current_list)
                continue
            # TODO: Warn
            tree.append(node)

        return tree

    def _find_list(self, root_node: dict, level: int, list_item: Optional[str] = None) -> Optional[dict]:
        filter_on_type = isinstance(list_item, str)
        if (
            root_node.get('_type') == 'list'
            and root_node.get('level') == level
            and (filter_on_type and root_node.get('listItem') == list_item)
        ):
            return root_node

        children = root_node.get('children')
        if children:
            return self._find_list(children[-1], level, list_item)

        return None

    def _list_from_block(self, block: dict) -> dict:
        return {
            '_type': 'list',
            '_key': f'${block["_key"]}-parent',
            'level': block.get('level'),
            'listItem': block['listItem'],
            'children': [block],
        }


def render(blocks: List[Dict], *args: Any, **kwargs: Any) -> str:
    """Shortcut function inspired by Sanity's own blocksToHtml.h callable."""
    renderer = PortableTextRenderer(blocks, *args, **kwargs)
    return renderer.render()
