"""The common parsing interface"""

from abc import ABC, abstractmethod
from pathlib import Path


class Parser(ABC):
    dotfile_dir: Path

    def __init__(self, dotfile_dir: Path):
        self.dotfile_dir = dotfile_dir

    @abstractmethod
    def parse(self) -> None:
        pass
