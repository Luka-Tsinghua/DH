"""Check repository Markdown links and image paths without network access."""

from __future__ import annotations

import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".venv", "venv", "build", "dist", "node_modules", ".pytest_cache"}


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and name in {"href", "src"}:
                self.targets.append(value)
            if value and name in {"id", "name"}:
                self.anchors.add(value)


def without_code(text: str) -> str:
    lines = []
    fence = ""
    for line in text.splitlines():
        match = re.match(r"\s*(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if not fence:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = ""
            continue
        if not fence:
            lines.append(line)
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    text = without_code(text)
    parser = Links()
    parser.feed(text)
    found = parser.anchors
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        heading = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).replace("`", "")
        slug = "".join(char for char in heading.lower()
                       if char in "-_ " or not unicodedata.category(char).startswith(("P", "S")))
        slug = slug.replace(" ", "-")
        candidate = slug
        suffix = 0
        while candidate in found:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        found.add(candidate)
    return found


def check(root: Path = REPO_ROOT) -> list[str]:
    errors = []
    link_count = 0
    documents = sorted(path for path in root.rglob("*.md")
                       if not any(part in SKIP_DIRS or part.endswith(".egg-info")
                                  for part in path.relative_to(root).parts))
    for document in documents:
        text = without_code(document.read_text(encoding="utf-8-sig"))
        parser = Links()
        parser.feed(text)
        targets = parser.targets + re.findall(r"!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+\"[^\"]*\")?\)", text)
        for target in targets:
            link_count += 1
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            path = (document.parent / unquote(url.path)).resolve() if url.path else document
            label = document.relative_to(root).as_posix()
            if not path.is_relative_to(root.resolve()) or not path.exists():
                errors.append(f"{label}: missing local target {target}")
            elif url.fragment and path.suffix.lower() == ".md":
                if unquote(url.fragment) not in anchors(path.read_text(encoding="utf-8-sig")):
                    errors.append(f"{label}: missing anchor {target}")
    print(f"Checked {link_count} links across {len(documents)} Markdown files.")
    return errors


def main() -> None:
    errors = check()
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print("Local documentation links passed.")


if __name__ == "__main__":
    main()
