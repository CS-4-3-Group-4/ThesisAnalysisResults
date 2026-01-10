"""
Statistical Significance Testing modules (SOP 3 & 4).
Contains statistical significance tests (paired t-tests) for fitness, time, memory, and solution quality metrics.
"""

from . import fitness
from . import time
from . import memory
from . import solution_quality

__all__ = ["fitness", "time", "memory", "solution_quality"]
