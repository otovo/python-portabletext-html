from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from portabletext_html.utils import get_default_marker_definitions

if TYPE_CHECKING:
    from typing import Literal, Optional, Tuple, Type, Union

    from portabletext_html.marker_definitions import MarkerDefinition


@dataclass(frozen=True)
class Span:
    """Class representation of a Portable Text span.

    A span is the standard way to express inline text within a block.
    """

    _type: Literal['span']
    text: str

    _key: Optional[str] = None
    marks: list[str] = field(default_factory=list)  # keys that correspond with block.mark_definitions
    style: Literal['normal'] = 'normal'


@dataclass
class Block:
    """Class representation of a Portable Text block.

    A block is what's typically recognized as a section of a text, e.g. a paragraph or a heading.

    listItem and markDefs are camelCased to support dictionary unpacking.
    """

    _type: Literal['block']

    _key: Optional[str] = None
    style: Literal['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'normal'] = 'normal'
    level: Optional[int] = None
    listItem: Optional[Literal['bullet', 'number', 'square']] = None
    children: list[dict] = field(default_factory=list)
    markDefs: list[dict] = field(default_factory=list)
    marker_definitions: dict[str, Type[MarkerDefinition]] = field(default_factory=dict)
    marker_frequencies: dict[str, int] = field(init=False)

    def __post_init__(self) -> None:
        """
        Add custom fields after init.

        To make handling of span `marks` simpler, we define marker_definitions as a dict, from which
        we can directly look up both annotation marks or decorator marks.
        """
        self.marker_definitions = self._add_custom_marker_definitions()
        self.marker_frequencies = self._compute_marker_frequencies()

    def _compute_marker_frequencies(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for child in self.children:
            for mark in child.get('marks', []):
                if mark in counts:
                    counts[mark] += 1
                else:
                    counts[mark] = 0
        return counts

    def _add_custom_marker_definitions(self) -> dict[str, Type[MarkerDefinition]]:
        marker_definitions = get_default_marker_definitions(self.markDefs)
        marker_definitions.update(self.marker_definitions)
        for definition in self.markDefs:
            if definition['_type'] in self.marker_definitions:
                marker = self.marker_definitions[definition['_type']]
                marker_definitions[definition['_key']] = marker
                del marker_definitions[definition['_type']]
        return marker_definitions

    def get_node_siblings(self, node: Union[dict, Span]) -> Tuple[Optional[dict], Optional[dict]]:
        """Return the sibling nodes (prev, next) to the given node."""
        if not self.children:
            return None, None
        try:
            if type(node) == dict:
                node_idx = self.children.index(node)
            elif type(node) == Span:
                for index, item in enumerate(self.children):
                    if 'text' in item and node.text == item['text']:
                        # Is it possible to handle several identical texts?
                        node_idx = index
                        break
            else:
                raise ValueError(f'Expected dict or Span but received {type(node)}')
        except ValueError:
            return None, None

        next_node = None

        prev_node = self.children[node_idx - 1] if node_idx != 0 else None
        if node_idx != len(self.children) - 1:
            next_node = self.children[node_idx + 1]

        return prev_node, next_node
