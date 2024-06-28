# GreNeoGraphQL

GreNeoGraphQL is a vulnerability database language based on code graph database queries. Currently, it supports converting Python source code into CFG (Control Flow Graph) and importing it into the database for specific queries. Other functionalities are still under development.

## Usage

> You should work right under `code2Graph/` directory, which is the root..

### Configure Global Variables

Create a file named config.yaml in the root directory of the project, and fill in the following content:

```yaml
PROJECT_PATH: "./tmp/proj/demo"
BACKEND:
  DATABASE: "gremlin"
  GREMLIN:
    CONNECTION_STRING: "ws://<gremlin_ip>:8182/gremlin"
  HUGEGRAPH:
    CONNECTION_STRING: "<hugegraph_ip>"
  FILEDB:
    VERTEX_FILE: "./tmp/vertex.json"
    EDGE_FILE: "./tmp/edge.json"
CACHE:
  DATABASE: "memory"
  REDIS:
    HOST: "<redis_ip>"
    PORT: 6379
    DB: <redis_database_id>
    PASSWORD: <redis_password>
```

- `PROJECT_PATH` is the path to your project. It can be overridden with command-line arguments.
- For `BACKEND`, you can choose `DATABASE` from `gremlin`, `hugegraph` and `filedb`. And fill in the corresponding connection string.
- For `CACHE`, you can choose `DATABASE` from `memory` and `redis`. And fill in the corresponding redis connection information. If you use Redis, you should fill the `REDIS` section, set `PASSWORD` to `null` if you don't have a password.

### 2.2 Build Graph

See help for `build.sh`, or you can directly run `src/py2graph.py` to get more options. For detailed usage, see both files respectively.

## BUG List

- [*] `src/py2cfg.py` may miss some vertices when add edges.