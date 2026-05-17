"""Compatibility wrapper for the canonical Table 1 generator.

Table 1 now uses the same drop + feature-decomposition feature set as
Table 2 and Table 3. Running this legacy entry point regenerates both
online-activity and psychological-distress Table 1 outputs with the
current canonical logic.
"""
from __future__ import annotations

from build_table1_drop_decomposition import main


if __name__ == "__main__":
    main()
