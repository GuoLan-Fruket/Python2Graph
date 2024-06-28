class CgDb:
    def __init__(self) -> None:
        self.caller = {}
        self.callee = {}


CG_DB = CgDb()


def get_cg_db() -> CgDb:
    return CG_DB
