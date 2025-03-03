# benchmark/__init__.py

"""
This package re-exports key functions from the submodules for ease of use.
Modules included:
  - scheduler: Functions for safe iteration execution and scheduling.
  - sizes: Functions for generating array sizes and determining worker counts.
  - processor: Functions for processing array sizes and running the benchmark tests.
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
