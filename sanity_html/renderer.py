from __future__ import annotations

import html
from typing import TYPE_CHECKING

from sanity_html.constants import STYLE_MAP
from sanity_html.dataclasses import Block, Span
from sanity_html.marker_definitions import DefaultMarkerDefinition
from sanity_html.utils import get_list_tags, is_block, is_list, is_span

if TYPE_CHECKING:
    from typing import Callable, Dict, List, Optional, Type, Union

    from sanity_html.marker_definitions import MarkerDefinition


# TODO: Let user pass custom code block definitions/plugins
#  to represent custom types (see children definition in portable text spec)


class SanityBlockRenderer:
    """HTML renderer for Sanity block content."""

    def __init__(
        self,
        blocks: Union[list[dict], dict],
        custom_marker_definitions: dict[str, Type[MarkerDefinition]] = None,
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
        list_nodes: List[Dict] = []
        for node in self._blocks:

            if list_nodes and not is_list(node):
                tree = self._normalize_list_tree(list_nodes, Block(**node))
                result += ''.join([self._render_node(n, Block(**node), list_item=True) for n in tree])
                list_nodes = []  # reset list_nodes

            if is_list(node):
                list_nodes.append(node)
                continue  # handle all elements ^ when the list ends

            result += self._render_node(node)  # render non-list nodes immediately

        if list_nodes:
            tree = self._normalize_list_tree(list_nodes, Block(**node))
            result += ''.join(
                self._render_node(n, Block(**node), list_item=True) for n in tree
            )


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
            block = Block(**node, marker_definitions=self._custom_marker_definitions)
            return self._render_list(block, context)
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
            return self._render_span(span, block=context)  # context is span's outer block
        elif custom_serializer := self._custom_serializers.get(node.get('_type', '')):
            return custom_serializer(node, context, list_item)
        else:
            print('Unexpected code path 👺')  # noqa: T001 # TODO: Remove after thorough testing
            return ''

    def _render_block(self, block: Block, list_item: bool = False) -> str:
        text = ''
        if not list_item:
            tag = STYLE_MAP[block.style]
            text += f'<{tag}>'

            for child_node in block.children:
                text += self._render_node(child_node, context=block)
            text += f'</{tag}>'
        else:
            for child_node in block.children:
                text += self._render_node(child_node, context=block)
        return text

    def _render_span(self, span: Span, block: Block) -> str:
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

    def _normalize_list_tree(self, nodes: list, block: Block) -> list[dict]:
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
                    current_list.children.append(node)
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


def render(blocks: List[Dict]) -> str:
    """Shortcut function inspired by Sanity's own blocksToHtml.h callable."""
    renderer = SanityBlockRenderer(blocks)
    return renderer.render()
