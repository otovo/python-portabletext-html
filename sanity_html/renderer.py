import html


class SanityBlockRenderer:
    """HTML renderer for Sanity block content."""

    def __init__(self, blocks: list[dict]) -> None:
        self._blocks = blocks

    @staticmethod
    def render(blocks: list[dict]) -> str:
        """Render the given list of blocks to HTML."""
        renderer = SanityBlockRenderer(blocks)
        return renderer._render()

    def _render(self) -> str:
        result = ''
        for block in self._blocks:
            if block['_type'] == 'block':
                result += self._render_block(block)
        return result

    def _render_block(self, block: dict) -> str:
        block_tag = 'p'
        result = f'<{block_tag}>'
        children: list[dict] = block.get('children', [])

        for idx, current_child in enumerate(children):
            previous_child = children[idx - 1] if idx >= 1 else None
            previous_marks = previous_child.get('marks', []) if previous_child else []

            next_child = children[idx + 1] if idx < len(children) - 1 else None
            next_marks = next_child.get('marks', []) if next_child else []

            if current_child.get('_type') == 'span':
                marks: list[str] = current_child.get('marks', [])
                for mark in marks:
                    # The previous sibling opened the tag, so we don't need to
                    # open a new one.
                    if mark in previous_marks:
                        continue
                    result += f'<{mark}>'

                result += html.escape(current_child['text'])
                for mark in reversed(marks):
                    if mark in next_marks:
                        continue
                    result += f'</{mark}>'

        result += f'</{block_tag}>'
        return result
