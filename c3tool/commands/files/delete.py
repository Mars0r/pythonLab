"""Delete one file or symbolic link without recursive removal."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("del", "<filepath>", "Deletes one file or symbolic link.", "python3 script.py del <filepath>", "A deletion confirmation.", "c3tool.commands.files.delete:DeleteCommand", order=4)


class DeleteCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Safely delete exactly one file or symbolic link.
        # 1. Require one path and resolve it with ``expand_path``.
        self.require_count(args, 1, COMMAND_SPEC.usage)
        path = expand_path(args[0], context)
        # 2. Refuse normal directories; this exercise must never delete trees.
        if path.is_dir():
            raise CommandError("Cannot delete directories with the 'del' command.")
        # 3. Report a missing path with CommandError.
        if not path.exists():
            raise CommandError(f"File not found: {path}")
        # 4. Unlink the target and return a confirmation.
        path.unlink()
        return f"Deleted: {path}"
