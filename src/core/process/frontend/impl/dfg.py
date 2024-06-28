"""
Core function to build DFG.
"""

from core.process.frontend.impl.dfg_lib.build import (
    build_dependencies,
    build_ssa,
    extract_paths,
)
from core.process.frontend.impl.dfg_lib.index import (
    index_constant,
    index_dependency,
    index_ssa,
    mend_ssa,
)
from core.process.frontend.impl.dfg_lib.index_collection import (
    ConstantCollection,
    DependencyCollection,
    SSA_Collection,
)
from core.process.frontend.common import get_frontend_producer, count_python_files
from lib.shared.task_util import Task, get_cpu_count
from lib.shared.logger import logger
from lib.shared.path_util import (
    get_file_name,
    get_relative_path,
)
from core.process.frontend.frontend import FrontEndDescriptor
from core.process.collector import Collector
from core.graph.graph import GraphEdge, GraphVertex
from scalpel.cfg import CFGBuilder


def _build_dfg_for_single_file(root: str, file: str, sink: Collector.Sink):
    logger().info(f"Building DFG for: {file}")

    # Initialize CFG
    # Here, we have to use flattened CFG to get detailed information
    # of function def (inner block)
    flattened_cfg = CFGBuilder().build_from_file(
        get_file_name(file), file, flattened=True
    )

    # Generate SSA
    ssa_results, const_dict = build_ssa(flattened_cfg)

    # mend SSA dependency
    mend_ssa(flattened_cfg, ssa_results, const_dict)

    # Get line dependency
    deps_collection: DependencyCollection = index_dependency(flattened_cfg)

    # Index all SSA constants
    ssa_const_collection: ConstantCollection = index_constant(const_dict)

    # Index all SSA dependencies
    ssa_deps_collection: SSA_Collection = index_ssa(ssa_results)

    # build dependencies
    dependencies = build_dependencies(
        deps_collection, ssa_deps_collection, ssa_const_collection
    )

    # Get simple paths
    paths = extract_paths(dependencies)

    # Add edges.
    file = get_relative_path(file, root)
    for path in paths:
        if path[0] == path[1]:
            continue
        from_v = GraphVertex("code", {"file": file, "lineno": path[0]})
        to_v = GraphVertex("code", {"file": file, "lineno": path[1]})
        sink.put_edge(GraphEdge("dfg", from_v, to_v))


def get_dfg_frontend_descriptor(
    root: str, producer: Task, sink: Collector.Sink, max_workers=None
) -> FrontEndDescriptor:
    """
    Get the descriptor for DFG frontend process.
    """
    if max_workers is None or max_workers <= 0:
        max_workers = max(1, min(get_cpu_count(), count_python_files(root) // 4))
    return FrontEndDescriptor(
        root=root,
        producer=producer,
        consumer=Task(_build_dfg_for_single_file),
        sink=sink,
        max_workers=max_workers,
    )
