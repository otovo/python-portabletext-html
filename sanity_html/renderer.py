from __future__ import annotations

import html
from typing import TYPE_CHECKING

from sanity_html.constants import STYLE_MAP
from sanity_html.dataclasses import Block, Span
from sanity_html.marker_definitions import render_link_marker
from sanity_html.utils import get_list_tags, is_block, is_list, is_span

if TYPE_CHECKING:
    from typing import Dict, List, Optional


# TODO: Let user pass custom code block definitions/plugins
#  to represent custom types (see children definition in portable text spec)


class SanityBlockRenderer:
    """HTML renderer for Sanity block content."""

    def __init__(self, blocks: list[dict]) -> None:
        self._blocks = blocks

    def render(self) -> str:
        """Render HTML from self._blocks."""
        rendered_html = ''
        list_nodes: List[Dict] = []
        for node in self._blocks:

            if list_nodes and not is_list(node):
                rendered_html += self._render_list(list_nodes)
                list_nodes = []  # reset list_nodes

            if is_list(node):
                list_nodes.append(node)
                continue  # handle all elements ^ when the list ends

            rendered_html += self._render_node(node)  # render non-list nodes immediately

        return rendered_html

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
                # I'm not 100% sure if this code path is possible, but the sanity lib checks for string type
                # https://github.com/sanity-io/block-content-to-hyperscript/blob/master/src/blocksToNodes.js#L114
                # so I would imagine it is
                # TODO: Remove if we can't justify this condition
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
            text += f'</{tag}>\n'
        else:
            for child_node in block.children:
                text += self._render_node(child_node, context=block)
        return text

    def _render_span(self, span: Span, block: Block) -> str:
        text = html.escape(span.text)

        for mark in span.marks:
            marker_callable = block.marker_definitions[mark]
            if marker_callable == render_link_marker:
                text = marker_callable(text=text, href=block.marker_definitions[span.marks[0]])
            else:
                text = marker_callable(text=text)

        return text

    def _render_list(self, nodes: list) -> str:
        html = ''
        tag_dict = {}
        for index, node in enumerate(nodes):

            current_level = node['level']
            prev_level = nodes[index - 1]['level'] if index > 0 else None

            list_item = node.pop('listItem')  # this lets us call render_node for non-list handling
            list_tags = get_list_tags(list_item)
            node_inner_html = '<li>' + ''.join(list(self._render_node(node, list_item=True))) + '</li>'

            if not html:  # first item
                html += list_tags[0]
                tag_dict[current_level] = list_tags[1]  # add closing tag to the map which should be empty at the end
                html += node_inner_html
                continue

            if current_level == prev_level:
                html += node_inner_html
                continue

            if current_level > prev_level:
                html += list_tags[0]
                tag_dict[current_level] = list_tags[1]  # add closing tag to the map which should be empty at the end
                html += node_inner_html
                continue

            if current_level < prev_level:
                html += tag_dict.pop(prev_level)  # time to close tags
                html += node_inner_html
                continue

        # make sure to close off the last tag
        html += tag_dict.pop(list(tag_dict.keys())[0])

        assert tag_dict == {}
        return html


def render(blocks: List[Dict]) -> str:
    """Shortcut function inspired by Sanity's own blocksToHtml.h callable."""
    renderer = SanityBlockRenderer(blocks)
    return renderer.render()
