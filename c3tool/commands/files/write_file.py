"""Write text to a file."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandSpec, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("writeFile", "<filename> <text>", "Writes text to a file.", "python3 script.py writeFile <filename> <text>", "A confirmation containing the written path.", "c3tool.commands.files.write_file:WriteFileCommand", order=2)


class WriteFileCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Write user-provided text to a path.
        # 1. Require a filename plus at least one text argument.
        self.require_range(args, 2, 1000, COMMAND_SPEC.usage)
        # 2. Resolve the filename with ``expand_path``.
        expanded_path = expand_path(args[0], context)
        # 3. Join all remaining arguments so spaces in the text are preserved.
        text = " ".join(args[1:])
        # 4. Create missing parent folders, write UTF-8 text, and confirm the path.
        #    Use ``path.parent.mkdir(parents=True, exist_ok=True)`` to create folders.
        expanded_path.parent.mkdir(parents=True, exist_ok=True)
        expanded_path.write_text(text, encoding="utf-8")
        return f"Wrote to {expanded_path}"
