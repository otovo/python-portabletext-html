import html


class SanityBlockRenderer:
    def __init__(self, blocks: list[dict]) -> None:
        self._blocks = blocks

    @classmethod
    def render(cls, blocks: list[dict]) -> str:
        renderer = SanityBlockRenderer(blocks)
        return renderer._render()

    def _render(self) -> str:
        result = ""
        for block in self._blocks:
            if block["_type"] == "block":
                result += self._render_block(block)
        return result

    def _render_block(self, block):
        block_tag = "p"
        result = f"<{block_tag}>"
        for child in block.get("children", []):
            if child.get("_type") == "span":
                result += html.escape(child["text"])
        result += f"</{block_tag}>"
        return result
