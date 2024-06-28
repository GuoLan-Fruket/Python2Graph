import json
import os

import yaml
from core.cache.cache_proxy import CacheProxy
from core.db.filedb.connection import get_filedb_client, resolve_filedb
from core.db.gremlin.connection import get_gremlin_client, resolve_gremlin


def get_backend_client(config: dict, cache: CacheProxy):
    db = str(config["DATABASE"]).lower()
    if db == "gremlin":
        resolve_gremlin(config["GREMLIN"])
        return get_gremlin_client(cache)
    if db == "hugegraph":
        raise Exception("HugeGraph is not supported yet.")
    if db == "filedb":
        resolve_filedb(config["FILEDB"])
        return get_filedb_client()
    raise Exception(f"Database {db} is not supported.")


def get_worker_count(worker_count):
    if worker_count is None or worker_count <= 0:
        return None
    return worker_count


def get_batch_size(batch_size):
    if batch_size is None or batch_size <= 0:
        return None
    return batch_size


class CommitDiff:
    def __init__(self):
        self.added = []
        self.removed = []
        self.modified = []

    @classmethod
    def load(cls, file):
        ext = os.path.splitext(file)[1]
        if ext == ".json":
            return cls._load_from_json(file)
        if ext == ".yaml" or ext == ".yml":
            return cls._load_from_yaml(file)
        return None

    @classmethod
    def _load_from_yaml(cls, file):
        with open(file) as f:
            return cls._load_from_dict(yaml.safe_load(f))

    @classmethod
    def _load_from_json(cls, file):
        with open(file) as f:
            return cls._load_from_dict(json.load(f))

    @classmethod
    def _load_from_dict(cls, data):
        diff = cls()
        diff.added = data.get("added", [])
        diff.removed = data.get("removed", [])
        diff.modified = data.get("modified", [])
        return diff

    def all(self):
        return self.added + self.removed + self.modified

    def enumerate(self):
        for file in self.added:
            yield file, "A"
        for file in self.removed:
            yield file, "R"
        for file in self.modified:
            yield file, "M"
            