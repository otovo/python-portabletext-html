from __future__ import annotations

from typing import TYPE_CHECKING
import html

from sanity_html.constants import DECORATOR_MARKER_SERIALIZERS
from sanity_html.marker_serializers import DefaultMarkerSerializer
from sanity_html.types import Span

if TYPE_CHECKING:
    from typing import Optional, Union
    from sanity_html.renderer import SanityBlockRenderer
    from sanity_html.types import Block


class SpanSerializer:
    def __init__(self, sanity_renderer: SanityBlockRenderer) -> None:
        self.sanity_renderer = sanity_renderer

    def __call__(self, span: Union[dict, str], block: Block, child_idx: Optional[int] = None):
        if isinstance(span, str):
            span = Span(**{'text': span})
        else:
            span = Span(**span)

        result: str = ''
        prev_node, next_node = block.get_node_siblings(span, child_idx=child_idx)
        prev_marks = prev_node.get('marks', []) if prev_node else []
        next_marks = next_node.get('marks', []) if next_node else []

        sorted_marks = sorted(
            span.marks, key=lambda x: (int(x in DECORATOR_MARKER_SERIALIZERS), -block.marker_frequencies[x])
        )
        for mark in sorted_marks:
            if mark in prev_marks:
                continue
            marker_callable = block.marker_definitions.get(mark)()
            result += marker_callable.render_prefix(span, mark, block)

        result += html.escape(span.text).replace('\n', '<br/>')

        for mark in reversed(sorted_marks):
            print(child_idx, mark, 'in', next_marks, next_node)
            if mark in next_marks:
                continue

            marker_callable = block.marker_definitions.get(mark, DefaultMarkerSerializer)()
            result += marker_callable.render_suffix(span, mark, block)

        return result
