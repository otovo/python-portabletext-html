from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    SanityIdType = Optional[str]  # represents a [:13] uuid hex
