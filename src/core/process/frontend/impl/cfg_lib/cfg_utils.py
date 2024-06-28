from core.process.collector import Collector


class CfgBuildCtx:
    def __init__(self, file: str, sink: Collector.Sink) -> None:
        self.file = file
        self.sink: Collector.Sink = sink
        self.visited_block_first = {}
        self.visited_block_last = {}
        self.function_def_dic = {}
