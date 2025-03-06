# __init__.py

"""
benchmark package

This package provides the core functionality for the Sorting Algorithms Benchmark application.
It re-exports key functions, classes, and constants from submodules so that users can import everything
from a single location.

Modules included:
  - scheduler: Safe iteration execution and scheduling.
  - sizes: Functions for generating array sizes and determining worker counts.
  - processor: Functions for processing benchmark tests and aggregating results.
  - algorithms_map: Mapping of algorithm names to sorting functions.
  - config: Global configuration settings and debug support.
  - csv_utils: Utilities for CSV file operations.
  - markdown_utils: Functions for generating markdown reports.
  - exit_handlers: Graceful shutdown handling.
  - utils: General helper functions.
"""

from .scheduler import (
    safe_run_target,
    safe_run_iteration,
    update_missing_iterations_concurrent,
)
from .sizes import (
    generate_sizes,
    get_num_workers,
)
from .processor import (
    update_overall_results,
    process_size,
    run_sorting_tests,
)
from .algorithms_map import (
    get_algorithms,
)
from .config import (
    debug,
    VERBOSE,
    SLOW_MODE,
    DEFAULT_ITERATIONS,
    DEFAULT_THRESHOLD,
)
from .csv_utils import (
    read_csv_results,
    ensure_csv_ends_with_newline,
    sort_csv_alphabetically,
    get_csv_results_for_size,
)
from .markdown_utils import (
    write_markdown,
    write_algorithm_markdown,
    rebuild_readme,
)
from .exit_handlers import (
    shutdown_requested,
)
from .utils import (
    format_time,
    group_rankings,
    run_iteration,
    compute_average,
    compute_median,
    ordinal,
    format_size,
)

__all__ = [
    # scheduler functions
    "safe_run_target",
    "safe_run_iteration",
    "update_missing_iterations_concurrent",
    # sizes functions
    "generate_sizes",
    "get_num_workers",
    # processor functions
    "update_overall_results",
    "process_size",
    "run_sorting_tests",
    # algorithms_map functions
    "get_algorithms",
    # config variables and functions
    "debug",
    "VERBOSE",
    "SLOW_MODE",
    "DEFAULT_ITERATIONS",
    "DEFAULT_THRESHOLD",
    # csv_utils functions
    "read_csv_results",
    "ensure_csv_ends_with_newline",
    "sort_csv_alphabetically",
    "get_csv_results_for_size",
    # markdown_utils functions
    "write_markdown",
    "write_algorithm_markdown",
    "rebuild_readme",
    # exit_handlers functions/variables
    "shutdown_requested",
    # utils functions
    "format_time",
    "group_rankings",
    "run_iteration",
    "compute_average",
    "compute_median",
    "ordinal",
    "format_size",
]
