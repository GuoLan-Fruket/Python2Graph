"""
Main module for the Python2Graph project.

usage: py2graph.py [-h] [-p PROJECT] [-c CONFIG] [--calc-thread CALC_THREAD]
                   [--io-thread IO_THREAD] [--v-batch V_BATCH] [--e-batch E_BATCH] [-f] [-b]
                   [-l (DEBUG|INFO|WARNING|ERROR|CRITICAL)]

Convert Python code to graph, and store in graph database.

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Path to the project
  -c CONFIG, --config CONFIG
                        Path to the configuration file
  --calc-thread CALC_THREAD
                        Number of threads for calculating
  --io-thread IO_THREAD
                        Number of threads for IO
  --v-batch V_BATCH     Number of vertices in a batch
  --e-batch E_BATCH     Number of edges in a batch
  -f, --force           If true, will clear previous database
  -b, --build           Only build the graph with this flag set
  -l (DEBUG|INFO|WARNING|ERROR|CRITICAL), --log (DEBUG|INFO|WARNING|ERROR|CRITICAL)
                        Log level, by default is INFO
"""

import yaml
from core.cache.connection import get_cache_proxy, resolve_cache
from core.process.backend.backend import get_backend_descriptor
from core.process.backend.backend_diff import apply_diff
from core.process.collector import Collector
from core.process.frontend.common import get_all_files_task, get_specified_files_task
from core.process.frontend.impl.cfg import get_cfg_frontend_descriptor
from lib.conf import CommitDiff, get_backend_client, get_batch_size, get_worker_count
from lib.shared.logger import logger, set_log_level
from core.process.frontend.impl.dfg import get_dfg_frontend_descriptor
from lib.argument import parse_args
from lib.shared.path_util import format_path
from core.process.frontend.impl.cg import get_cg_frontend_descriptor

if __name__ == "__main__":
    # Parse argument.
    args = parse_args()

    # Set log level.
    set_log_level(args.log)

    # Loading configuration & Establishing connection.
    config_path = format_path(args.config)
    logger().info(f"Loading configuration from: {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if args.project is None:
        if config.get("PROJECT_PATH") is None:
            raise Exception("Project path is not specified.")
        args.project = config["PROJECT_PATH"]
    root = format_path(args.project)
    logger().info(f"Initializing project at: {root}")

    logger().info("Connecting to cache provider...")
    resolve_cache(config["CACHE"])
    cache = get_cache_proxy()

    client = get_backend_client(config["BACKEND"], cache)

    logger().info("Initializing pipe...")
    pipe = Collector()

    ############################################################
    # Following are actual works.
    input_file_task = get_all_files_task(root)

    if args.force:
        if args.diff is not None:
            logger().warning("Diff file is specified, force flag will be ignored.")
        else:
            logger().info("Purging previous database...")
            client.drop()
            client.init()
            logger().info("Purging cache...")
            cache.clear()
    if args.diff != None:
        logger().info("Loading diff file...")
        diff = CommitDiff.load(args.diff)
        if diff is None:
            raise Exception("Diff file is not supported.")
        logger().info("Applying diff...")
        affected_files = apply_diff(client, diff)
        print("Affected files: ", affected_files)
        if affected_files != None:
            input_file_task = get_specified_files_task(root, affected_files)

    if args.build:
        cfg_thread = (
            get_cfg_frontend_descriptor(
                root,
                input_file_task,
                pipe.as_sink(),
                get_worker_count(args.calc_thread),
            )
            .get_process()
            .invoke_async()
        )

        dfg_thread = (
            get_dfg_frontend_descriptor(
                root,
                input_file_task,
                pipe.as_sink(),
                get_worker_count(args.calc_thread),
            )
            .get_process()
            .invoke_async()
        )

        logger().info("Transferring to database...")
        back_thread = (
            get_backend_descriptor(
                client,
                pipe.as_source(),
                max_workers=get_worker_count(args.io_thread),
                vertex_batch_size=get_batch_size(args.v_batch),
                edge_batch_size=get_batch_size(args.e_batch),
            )
            .get_process()
            .invoke_async()
        )

        cfg_thread.join()
        get_cg_frontend_descriptor(root, pipe.as_sink()).get_process().invoke()
        dfg_thread.join()
        pipe.as_sink().seal()
        back_thread.join()

        logger().info("Database ready to go! :)")
