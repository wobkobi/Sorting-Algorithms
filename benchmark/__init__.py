# __init__.py

"""
benchmark package

This package re-exports key functions from submodules for simplified importing.

Modules included:
  - scheduler: Safe iteration execution and scheduling.
  - sizes: Array sizes and worker count functions.
  - processor: Processing of benchmark tests and results aggregation.
"""

from .scheduler import (
    safe_run_target,
    safe_run_iteration,
    update_missing_iterations_concurrent,
)
from .sizes import generate_sizes, get_num_workers
from .processor import update_overall_results, process_size, run_sorting_tests

__all__ = [
    "safe_run_target",
    "safe_run_iteration",
    "update_missing_iterations_concurrent",
    "generate_sizes",
    "get_num_workers",
    "update_overall_results",
    "process_size",
    "run_sorting_tests",
]
