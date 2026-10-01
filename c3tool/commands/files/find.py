"""Recursively find partial filename matches."""

import os
from pathlib import Path

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("find", "<filename> <folder>", "Recursively finds partial filename matches.", "python3 script.py find <filename> <folder>", "Matching paths.", "c3tool.commands.files.find:FindCommand", order=20)


class FindCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Recursively search a folder for partial filename matches.
        # 1. Require a search fragment and a root folder.
        self.require_count(args, 2, COMMAND_SPEC.usage)
        search_fragment = args[0]
        root_folder = expand_path(args[1], context)
        # 2. Validate the folder before walking it.
        if not root_folder.is_dir():
            raise CommandError(f"Root folder not found: {root_folder}")
        # 3. Compare names case-insensitively and keep output deterministic.
        matches = []
        for file_path in root_folder.rglob("*"):
            if file_path.is_file() and search_fragment.lower() in file_path.name.lower():
                matches.append(file_path)
            if file_path.is_dir() and search_fragment.lower() in file_path.name.lower():
                matches.append(file_path)
        matches.sort(key=lambda p: str(p).lower())
        # 4. Return matching full paths or a helpful no-results message.
        if not matches:
            return f"No matches found for '{search_fragment}' in {root_folder}"
        return "File  Name\n" + "\n".join(f"{match.is_file():<5} {match}" for match in matches)
