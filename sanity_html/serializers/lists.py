from __future__ import annotations

from typing import TYPE_CHECKING

from sanity_html.types import Block
from sanity_html.utils import is_block, is_list

if TYPE_CHECKING:
    from collections import deque
    from typing import Optional

    from sanity_html import SanityBlockRenderer


class ListSerializer:
    def __init__(self, sanity_renderer: SanityBlockRenderer) -> None:
        self.sanity_renderer = sanity_renderer

    def __call__(self, node: dict, blocks: deque[dict]) -> str:
        result = ''
        list_items: list[dict] = [node]
        while blocks and is_list(blocks[0]):
            list_items.append(blocks.popleft())
        list_roots = self._normalize_list_tree(list_items)
        for list_root in list_roots:
            head, tail = self.get_list_tags(list_root['listItem'])
            result += head
            for child in list_root['children']:
                result += f'<li>{self.sanity_renderer._render_block(Block(**child), True)}</li>'
            result += tail
        return result

    def get_list_tags(self, list_item: str) -> tuple[str, str]:
        """Return the appropriate list tags for a given list item."""
        # TODO: Make it possible for users to pass their own maps, perhaps by adding this to the class
        # and checking optional class context variables defined on initialization.
        return {
            'bullet': ('<ul>', '</ul>'),
            'square': ('<ul style="list-style-type: square">', '</ul>'),
            'number': ('<ol>', '</ol>'),
        }[list_item]

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
