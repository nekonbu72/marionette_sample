import os
from os.path import join, getsize
from pathlib import Path

# cnt = 0
# for root, dirs, files in os.walk('C:\\Users\\s150209\\desktop'):

#     if len(files) > 0:
#         print(" " * cnt + "---files---")
#         for name in files:
#             print(" " * cnt + f"{root}\{name}")

#     if len(dirs) > 0:
#         print(" " * cnt + "---dirs---")
#         for name in dirs:
#             print(" " * cnt + f"{root}\{name}\\")

#     cnt = cnt + 1


p = Path('C:\\Users\\s150209\\desktop')
# for file_or_dir in p.iterdir():
#     print(file_or_dir)


class DirNode:
    def __init__(self, root: str, name: str, is_dir: bool, is_file: bool, children: list):
        self.root = root
        self.name = name
        self.is_dir = is_dir
        self.is_file = is_file
        self.children = children

    @staticmethod
    def create_from_path(p: Path):
        children = []
        if p.is_dir():
            for node in p.iterdir():
                children.append(DirNode.create_from_path(node))
        return DirNode(p.root, p.name, is_dir=p.is_dir(), is_file=p.is_file(), children=children)

    def __str__(self):
        return str(Path.joinpath(self.root, self.name))


dn = DirNode.create_from_path(p)
print(dn)
