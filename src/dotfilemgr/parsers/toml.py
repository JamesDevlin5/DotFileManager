import tomllib
from collections.abc import Iterator
from pathlib import Path

from dotfilemgr.common import Registry

from .parser import Parser


class TomlParser(Parser):
    SETUP_FILE_NAME = "setup.toml"
    setup_files: Iterator[Path]

    def __init__(self, dotfile_dir: Path):
        super().__init__(dotfile_dir)

    def find_files(self):
        self.setup_files = self.dotfile_dir.rglob(self.SETUP_FILE_NAME)

    def load_files(self):
        for setup_file in self.setup_files:
            with open(setup_file, "rb") as f:
                config = tomllib.load(f)
                for name, group in config["dotfiles"].items():
                    registry = Registry(name)
                    registry.add_associations(
                        {
                            Path(a["dot_file"]): Path(a["config_file"])
                            for a in group["associations"]
                        }
                    )
                    registry.add_extra_commands(group["commands"])

    def parse(self) -> None:
        self.find_files()
        self.load_files()
