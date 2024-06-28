"""
Argument parsing.
"""

import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="py2graph.py",
        description="Convert Python code to graph, and store in graph database.",
        epilog="Enjoy the program! :)",
    )
    parser.add_argument(
        "-p",
        "--project",
        type=str,
        default=None,
        required=False,
        help="Path to the project",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=False,
        default="./config.yaml",
        help="Path to the configuration file",
    )
    parser.add_argument(
        "-d",
        "--diff",
        type=str,
        required=False,
        default=None,
        help="Path to the diff file",
    )
    parser.add_argument(
        "--calc-thread",
        type=int,
        default=0,
        help="Number of threads for calculating",
    )
    parser.add_argument(
        "--io-thread",
        type=int,
        default=0,
        help="Number of threads for IO",
    )
    parser.add_argument(
        "--v-batch",
        type=int,
        default=500,
        help="Number of vertices in a batch",
    )
    parser.add_argument(
        "--e-batch",
        type=int,
        default=200,
        help="Number of edges in a batch",
    )
    parser.add_argument(
        "-f",
        "--force",
        default=True,
        action="store_true",
        help="If true, will clear previous database",
    )
    parser.add_argument(
        "-b",
        "--build",
        default=False,
        action="store_true",
        help="Only build the graph with this flag set",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=str,
        default="INFO",
        metavar="(DEBUG|INFO|WARNING|ERROR|CRITICAL)",
        help="Log level, by default is INFO",
    )
    return parser.parse_args()
