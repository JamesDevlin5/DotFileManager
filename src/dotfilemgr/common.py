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
    extra_commands: list[str]

    def __init__(self, name: str):
        self.name = name
        self.set_dotfile_base_dir(Path.home())
        self.set_config_base_dir(Path.home())
        self.links = {}
        self.extra_commands = []
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

    def add_extra_command(self, cmd: str) -> Self:
        self.extra_commands.append(cmd)
        return self

    def add_extra_commands(self, cmds: list[str]) -> Self:
        for cmd in cmds:
            self.add_extra_command(cmd)
        return self


class RegistryCommander:
    def __init__(self):
        pass

    def clean(self) -> None:
        """Removes all config files from the registry"""
        for registry in Registry._registry:
            for configfile in registry.links.values():
                configfile.unlink(missing_ok=True)

    def install(self) -> None:
        """Installs the symlinks connecting config files to dot files"""
        for registry in Registry._registry:
            for dotfile, configfile in registry.links.items():
                if not dotfile.exists():
                    print(f"Dotfile `{dotfile}` does not exist...")
                    continue
                configfile.parent.mkdir(parents=True, exist_ok=True)
                configfile.symlink_to(dotfile)
            for cmd in registry.extra_commands:
                import subprocess

                result = subprocess.run(cmd, shell=True)
                if result.returncode != 0:
                    print(f"Failed to execute `{cmd}`...")
