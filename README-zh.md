# Python2Graph

在项目根目录下创建一个名为 config.yaml 的文件，并填写以下内容：

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

- 对于 `BACKEND`，你可以从 `gremlin` 和 `filedb` 中选择 `DATABASE`，并填写相应的连接信息。
- 对于 `CACHE`，你可以从 `memory` 和 `redis` 中选择 `DATABASE`，并填写相应的 `redis` 连接信息。如果使用 `redis`，应该填写 `REDIS` 部分，没有密码的话将 `PASSWORD` 设置为 `null`。

### 构建图

查看 `build.sh` 的帮助，或者你可以直接运行 `src/py2graph.py` 以获取更多选项。详细用法请分别参考这两个文件。