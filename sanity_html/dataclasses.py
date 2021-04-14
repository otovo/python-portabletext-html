from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

from sanity_html.utils import get_marker_definitions

if TYPE_CHECKING:
    from typing import Literal, Optional, Tuple, Type, Union

    from sanity_html.marker_definitions import MarkerDefinition
    from sanity_html.types import SanityIdType


@dataclass(frozen=True)
class Span:
    """Class representation of a Portable Text span.

    A span is the standard way to express inline text within a block.
    """

    _type: Literal['span']
    text: str

    _key: SanityIdType = None
    marks: list[str] = field(default_factory=list)  # keys that correspond with block.mark_definitions
    style: Literal['normal'] = 'normal'


@dataclass
class Block:
    """Class representation of a Portable Text block.

    A block is what's typically recognized as a section of a text, e.g. a paragraph or a heading.

    listItem and markDefs are camelCased to support dictionary unpacking.
    """

    _type: Literal['block']

    _key: SanityIdType = None
    style: Literal['h1', 'h2', 'h3', 'h4', 'normal'] = 'normal'
    level: Optional[int] = None
    listItem: Optional[Literal['bullet', 'number', 'square']] = None
    children: list[dict] = field(default_factory=list)
    markDefs: list[dict] = field(default_factory=list)
    marker_definitions: dict[str, Type[MarkerDefinition]] = field(init=False)

    def __post_init__(self) -> None:
        """
        Add custom fields after init.

        To make handling of span `marks` simpler, we define marker_definitions as a dict, from which
        we can directly look up both annotation marks or decorator marks.
        """
        self.marker_definitions = get_marker_definitions(self.markDefs)

    def get_node_siblings(self, node: Union[dict, Span]) -> Tuple[Optional[dict], Optional[dict]]:
        """Return the sibling nodes (prev, next) to the given node."""
        if not self.children:
            return (None, None)
        try:
            if type(node) == dict:
                node = cast(dict, node)
                node_idx = self.children.index(node)
            elif type(node) == Span:
                node = cast(Span, node)
                node_idx = self.children.index(next((c for c in self.children if c.get('_key') == node._key), {}))
        except ValueError:
            return (None, None)

        prev_node = None
        next_node = None

        if node_idx >= 1:
            prev_node = self.children[node_idx - 1]
        if node_idx < len(self.children) - 2:
            next_node = self.children[node_idx + 1]

        return (prev_node, next_node)
