"""List one directory."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("ls", "<filepath, default current>", "Lists a directory.", "python3 script.py ls [filepath]", "Directory entries with type and size.", "c3tool.commands.files.list:ListCommand", order=8)


class ListCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List either the supplied directory or ``context.cwd``.
        # 1. Accept zero or one argument and validate that the target is a folder.
        self.require_count(args, 1, COMMAND_SPEC.usage)
        # 2. Sort entries consistently so output is predictable on every OS.
        expanded_path = expand_path(args[0] if args else ".", context)
        # 3. Show a useful type, size, and name for each item.
        print("Type  Size       Name")
        for child in expanded_path.iterdir():
            if child.is_dir():
                type_str = "d---"
            elif child.is_file():
                type_str = "-rw-"
            else:
                type_str = "----"
            size_str = f"{child.stat().st_size} bytes" if child.is_file() else ""
            print(f"{type_str:5} {size_str:>10} {child.name}")

        # 4. Return a clear message for an empty directory.

