from __future__ import annotations

import html
from typing import TYPE_CHECKING

from sanity_html.constants import STYLE_MAP
from sanity_html.dataclasses import Block, Span
from sanity_html.marker_definitions import DefaultMarkerDefinition
from sanity_html.utils import get_list_tags, is_block, is_list, is_span

if TYPE_CHECKING:
    from typing import Dict, List, Optional, Union


# TODO: Let user pass custom code block definitions/plugins
#  to represent custom types (see children definition in portable text spec)


class SanityBlockRenderer:
    """HTML renderer for Sanity block content."""

    def __init__(self, blocks: Union[list[dict], dict]) -> None:
        self._wrapper_element: Optional[str] = None

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
                result += self._render_list(list_nodes)
                list_nodes = []  # reset list_nodes

            if is_list(node):
                list_nodes.append(node)
                continue  # handle all elements ^ when the list ends

            result += self._render_node(node)  # render non-list nodes immediately

        if list_nodes:
            result += self._render_list(list_nodes)

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
        if is_block(node):
            block = Block(**node)
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

    def _render_list(self, nodes: list) -> str:
        result, tag_dict = '', {}
        for index, node in enumerate(nodes):

            current_level = node['level']  # 1
            prev_level = nodes[index - 1]['level'] if index > 0 else 0  # default triggers first condition below

            list_item = node.pop('listItem')  # popping this attribute lets us call render_node for non-list handling
            node_inner_html = '<li>' + ''.join(list(self._render_node(node, list_item=True))) + '</li>'

            if current_level > prev_level:
                list_tags = get_list_tags(list_item)
                result += list_tags[0]
                result += node_inner_html
                tag_dict[current_level] = list_tags[1]
                continue

            elif current_level == prev_level:
                result += node_inner_html
                continue

            elif current_level < prev_level:
                result += node_inner_html
                result += tag_dict.pop(prev_level)
                continue

            else:
                print('Unexpected code path 🕵🏻‍')  # noqa: T001 # TODO: Remove or alter when done testing

        # there should be one or more tag in the dict for us to close off
        for value in tag_dict.values():
            result += value

        return result


def render(blocks: List[Dict]) -> str:
    """Shortcut function inspired by Sanity's own blocksToHtml.h callable."""
    renderer = SanityBlockRenderer(blocks)
    return renderer.render()
