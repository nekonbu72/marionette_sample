import pathlib
from typing import List


def load_scripts(dir: str) -> List[str]:
    scripts = []
    p = pathlib.Path(dir)
    if p.is_dir():
        for content in p.iterdir():
            script = __load_script(content)
            if len(script) > 0:
                scripts.append(script)
    return scripts


def __load_script(path: pathlib.Path) -> str:
    if path.is_file() and path.suffix == ".js":
        with open(str(path)) as f:
            script = str(f.read())
        return script
    return ""


def load_script(path: str) -> str:
    return __load_script(pathlib.Path(path))
