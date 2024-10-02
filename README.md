# Python2Graph

Create a file named config.yaml in the root directory of the project, and fill in the following content:

```yaml
BACKEND:
  DATABASE: "gremlin"
  GREMLIN:
    CONNECTION_STRING: "ws://<host>:8182/gremlin"
  FILEDB:
    VERTEX_FILE: "./tmp/vertex.json"
    EDGE_FILE: "./tmp/edge.json"
CACHE:
  DATABASE: "memory"
  REDIS:
    HOST: <host>
    PORT: 6379
    DB: <database>
    PASSWORD: <password>
```

- For `BACKEND`, you can choose `DATABASE` from `gremlin` and `filedb`. And fill in the corresponding connection string.
- For `CACHE`, you can choose `DATABASE` from `memory` and `redis`. And fill in the corresponding `redis` connection information. If you use `redis`, you should fill the `REDIS` section, set `PASSWORD` to `null` if you don't have a password.

### Build Graph

See help for `build.sh`, or you can directly run `src/py2graph.py` to get more options. For detailed usage, see both files respectively.
