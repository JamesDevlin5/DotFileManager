"""Common functions for installing dotfiles"""

from pathlib import Path
from typing import Self, TypeAlias

PathLike: TypeAlias = str | Path


class Registry:
    _registry: list["Registry"] = []

    name: str
    dotfiles_base_dir: Path
    config_base_dir: Path
    links: dict[Path, Path]

    def __init__(self, name: str):
        self.name = name
        self.set_dotfile_base_dir(Path.home())
        self.set_config_base_dir(Path.home())
        self.links = {}
        Registry._registry.append(self)

    def set_dotfile_base_dir(self, dir: PathLike) -> Self:
        self.dotfiles_base_dir = Path(dir)
        return self

    def set_config_base_dir(self, dir: PathLike) -> Self:
        self.config_base_dir = Path(dir)
        return self

    def set_base_dirs(self, dotfile_dir: PathLike, configfile_dir: PathLike) -> Self:
        self.set_dotfile_base_dir(dotfile_dir)
        self.set_config_base_dir(configfile_dir)
        return self

    def add_association(self, dotfile: PathLike, configfile: PathLike) -> Self:
        self.links[Path(dotfile)] = Path(configfile)
        return self

    def add_associations(self, associations: dict[PathLike, PathLike]) -> Self:
        for dotfile, configfile in associations.items():
            self.add_association(dotfile, configfile)
        return self
