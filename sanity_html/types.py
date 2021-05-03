from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

from sanity_html.constants import ANNOTATION_MARKER_SERIALIZERS, DECORATOR_MARKER_SERIALIZERS

if TYPE_CHECKING:
    from typing import Literal, Optional, Tuple, Type, Union

    from sanity_html.marker_serializers import MarkerSerializer


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
    marker_definitions: dict[str, Type[MarkerSerializer]] = field(default_factory=dict)
    marker_frequencies: dict[str, int] = field(init=False)

    def __post_init__(self) -> None:
        """
        Add custom fields after init.

        To make handling of span `marks` simpler, we define marker_definitions as a dict, from which
        we can directly look up both annotation marks or decorator marks.
        """
        marker_definitions = DECORATOR_MARKER_SERIALIZERS.copy()
        for definition in self.markDefs:
            if definition['_type'] in ANNOTATION_MARKER_SERIALIZERS:
                marker = ANNOTATION_MARKER_SERIALIZERS[definition['_type']]
                marker_definitions[definition['_key']] = marker
            if definition['_type'] in self.marker_definitions:
                marker = self.marker_definitions[definition['_type']]
                marker_definitions[definition['_key']] = marker

        marker_definitions.update(self.marker_definitions)
        self.marker_definitions = marker_definitions
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

    def get_node_siblings(
        self, node: Union[dict, Span], child_idx: Optional[int] = None
    ) -> Tuple[Optional[dict], Optional[dict]]:
        """Return the sibling nodes (prev, next) to the given node."""
        if not self.children:
            return None, None
        if child_idx is not None:
            node_idx = child_idx
        else:
            print('fallback')
            try:
                if not isinstance(node, (dict, Span)):
                    raise ValueError(f'Expected dict or Span but received {type(node)}')
                elif type(node) == dict:
                    node = cast(dict, node)
                    node_idx = self.children.index(node)
                elif type(node) == Span:
                    node = cast(Span, node)
                    node_idx = self.children.index(next((c for c in self.children if c.get('_key') == node._key), {}))
            except ValueError:
                return None, None

        prev_node = None
        next_node = None
        print(node_idx, self.children)
        print(node_idx, len(self.children), node_idx < len(self.children) - 2)
        if node_idx >= 1:
            prev_node = self.children[node_idx - 1]
        if node_idx <= len(self.children) - 2:
            next_node = self.children[node_idx + 1]

        return prev_node, next_node
