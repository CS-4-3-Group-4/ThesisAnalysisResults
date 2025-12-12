"""
Statistical Significance Testing modules (SOP 3 & 4).
Contains statistical significance tests (paired t-tests) for fitness, time, and memory metrics.
"""

from . import fitness
from . import time
from . import memory

__all__ = ["fitness", "time", "memory"]
