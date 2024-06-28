import ast
import json
import astor


def load_source_code(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
            return source_code
    except FileNotFoundError as e:
        print("File not found")
        raise e
    except Exception as e:
        print("Failed to read file")
        raise e


class AdvancedEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


def obj_dumps(obj, indent=4):
    if indent <= 0:
        return json.dumps(obj, cls=AdvancedEncoder)
    return json.dumps(obj, cls=AdvancedEncoder, indent=indent)


def dict_dumps(obj, indent=4):
    return json.dumps(obj, indent=indent)


def get_parent_module_name(module_name):
    """
    Get the parent module name of a module.
    """
    return ".".join(module_name.split(".")[:-1])


def split_module_name(module_name):
    """
    Split the module name into a list of module names.
    """
    parts = module_name.split(".")
    if len(parts) == 1:
        return "", parts[0]
    else:
        return ".".join(parts[:-1]), parts[-1]
