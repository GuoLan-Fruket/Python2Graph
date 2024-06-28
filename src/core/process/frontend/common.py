"""
This module contains the common frontend processing logic.
"""

import os
from lib.shared.task_util import Task
from lib.shared.path_util import enumerate_files, format_path


def list_all_python_files(path):
    """
    Get all python files in the given path in a list.
    """
    return list(enumerate_files(path, [".py"]))


def count_python_files(path):
    """
    Count the number of python files in the given path.
    """
    return len(list_all_python_files(path))


def get_frontend_producer(project_path):
    """
    Return the frontend producer task.
    It simply emits all python files in the given path.
    """
    return Task(enumerate_files, (project_path, [".py"]))


def get_all_files_task(project_path):
    """
    Return the frontend producer task.
    It simply emits all python files in the given path.
    """
    return Task(enumerate_files, (project_path, [".py"]))


def _enumerate_files(root, files):
    """
    Enumerate all files in the given path.
    """
    for file in files:
        yield format_path(os.path.join(root, file))


def get_specified_files_task(project_path, files):
    """
    Return the frontend producer task.
    It simply emits all python files in the given path.
    """
    return Task(_enumerate_files, (project_path, files))
