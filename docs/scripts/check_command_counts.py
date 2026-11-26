#!/usr/bin/env python3
"""Check that the counts in the command reference agree with the commands it lists.

The command reference (`docs/en/commands.md` and `docs/ja/commands.md`) states the
same numbers in several places: the totals in the opening paragraph, the rows of
the domain summary table, the `(N)` in sub-headings and the number of commands
that accept the play-world selector. This script reads both documents and
compares every stated number with the command rows that are actually listed.

Checks:

    K1  opening totals = domain summary totals = listed commands
    K2  each summary row = the commands of its domain section (both directions)
    K3  `(N)` in a sub-heading = the command rows in its range
    K4  a sub-heading with a count must have a command table with rows
    K5  English and Japanese agree
    K6  the play-world selector count = the names listed for it
    K7  the Demo column of the summary = the demo marks of the command rows
    K8  a fully-qualified command name is listed once per language

Exit codes:

    0  consistent
    1  inconsistent (at least one finding)
    2  no verdict (an input could not be read or judged; a check saw nothing)

Input modes:

    (default)         the staged content (`git show :docs/...`)
    --rev REV         the content at a commit (`git show REV:docs/...`)
    --worktree        the files in the working tree
    --en PATH --ja PATH --exceptions PATH
                      the given files; runs no git command at all

The standard output of `--json` is a machine-readable report (schema_version 1);
the human-readable text then goes to the standard error.

Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

# Version of the JSON report written by `--json`.
REPORT_SCHEMA_VERSION: Final = 1

# Version of the exception file this script understands.
EXCEPTIONS_SCHEMA_VERSION: Final = 1

# Repository-relative paths of the inputs.
ENGLISH_DOCUMENT_PATH: Final = "docs/en/commands.md"
JAPANESE_DOCUMENT_PATH: Final = "docs/ja/commands.md"
EXCEPTIONS_PATH: Final = "docs/scripts/command_count_exceptions.json"

# Exception kinds.
KIND_PROSE_ONLY_BRIDGE: Final = "prose-only-bridge"
KIND_SUBSET_HEADING: Final = "subset-heading"
EXCEPTION_KINDS: Final = (KIND_PROSE_ONLY_BRIDGE, KIND_SUBSET_HEADING)

# Environment variables that change how git interprets path arguments. They are
# dropped before running git so that the paths below mean what they say.
SCRUBBED_ENVIRONMENT_VARIABLES: Final = (
    "GIT_LITERAL_PATHSPECS",
    "GIT_GLOB_PATHSPECS",
    "GIT_NOGLOB_PATHSPECS",
    "GIT_ICASE_PATHSPECS",
)

# Hint printed after a failing run.
FIX_HINT: Final = (
    "How to fix: make the domain summary table and the section listings agree "
    "(edit whichever one is wrong). To add an exception, edit "
    "docs/scripts/command_count_exceptions.json and raise the entry limit in the "
    "contrast test (reviewed on purpose)."
)

_FENCE_PATTERN: Final = re.compile(r"^\s*(```|~~~)")
_HEADING_PATTERN: Final = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_DOMAIN_PREFIX_PATTERN: Final = re.compile(r"^(UAIP(?:\.[A-Za-z0-9_]+)+)")
_BACKTICK_PATTERN: Final = re.compile(r"`([^`]+)`")
_SEPARATOR_CELL_PATTERN: Final = re.compile(r"^:?-+:?$")
_PAREN_GROUP_PATTERN: Final = re.compile(r"[(（]([^()（）]*)[)）]")
_DECORATION_PATTERN: Final = re.compile("[\U0001F000-\U0001FFFF☀-➿️]")
_PARTIAL_DEMO_PATTERN: Final = re.compile(r"^(?:partial|一部)\s*[(（]\s*(\d+)\s*/\s*(\d+)\s*[)）]$")
_DIGIT_PATTERN: Final = re.compile(r"\d")


class NoVerdictError(Exception):
    """Raised when an input cannot be read or judged. The run ends with exit code 2."""


@dataclass(frozen=True)
class LanguageProfile:
    """Everything that differs between the English and the Japanese document."""

    # Language code: "en" or "ja".
    code: str

    # Accepted first-column header of a command table.
    command_header: str

    # Accepted last-column header of a command table.
    description_header: str

    # Text of the level-2 heading that opens the domain summary.
    summary_heading: str

    # Text of the level-2 heading that opens the play-world selector section.
    selector_heading: str

    # Header cells of the selector table: (domain column, commands column).
    selector_table_headers: tuple[str, str]

    # Pattern with one group: the number of commands that take the selector.
    selector_stated_pattern: re.Pattern[str]

    # Pattern with one group: the count of UAIP commands in the opening paragraph.
    intro_native_pattern: re.Pattern[str]

    # Pattern with one group: the count of Toolset bridge commands in the opening paragraph.
    intro_bridge_pattern: re.Pattern[str]

    # Pattern with one group: the combined total in the opening paragraph.
    intro_total_pattern: re.Pattern[str]

    # Pattern for a whole parenthesised group that states a count; group 1 is the number.
    count_group_pattern: re.Pattern[str]

    # Sentences that say the commands of the following table are not in the demo build.
    no_demo_phrases: tuple[str, ...]


ENGLISH_PROFILE: Final = LanguageProfile(
    code="en",
    command_header="Command",
    description_header="Description",
    summary_heading="Domain summary",
    selector_heading="Choosing which play world a Runtime command acts on",
    selector_table_headers=("Domain", "Commands"),
    selector_stated_pattern=re.compile(r"(\d+) Runtime commands therefore take"),
    intro_native_pattern=re.compile(r"(\d+) \*\*UAIP commands\*\*"),
    intro_bridge_pattern=re.compile(r"(\d+) \*\*Toolset bridge commands\*\*"),
    intro_total_pattern=re.compile(r"combined total of (\d+)"),
    count_group_pattern=re.compile(r"^\(\s*(\d+)\s*(?:,.*)?\)$"),
    no_demo_phrases=("Not provided in the demo build",),
)

JAPANESE_PROFILE: Final = LanguageProfile(
    code="ja",
    command_header="コマンド",
    description_header="説明",
    summary_heading="ドメインサマリ",
    selector_heading="実行時コマンドの対象プレイワールドを指定する",
    selector_table_headers=("ドメイン", "コマンド"),
    selector_stated_pattern=re.compile(r"そのため\s*(\d+)\s*個の実行時コマンドが"),
    intro_native_pattern=re.compile(r"(\d+) 個の \*\*UAIP コマンド\*\*"),
    intro_bridge_pattern=re.compile(r"(\d+) 個の \*\*Toolset ブリッジコマンド\*\*"),
    intro_total_pattern=re.compile(r"合計\s*(\d+)"),
    count_group_pattern=re.compile(r"^（\s*(\d+)\s*(?:件|コマンド)?\s*(?:、.*)?）$"),
    no_demo_phrases=("デモ版には含まれません", "デモ版では提供されません"),
)

PROFILES: Final = {"en": ENGLISH_PROFILE, "ja": JAPANESE_PROFILE}


@dataclass(frozen=True)
class Heading:
    """A Markdown heading."""

    # Number of leading `#` characters.
    level: int

    # Heading text without the `#` marks.
    text: str

    # 1-based line number.
    line: int


@dataclass(frozen=True)
class TableRow:
    """A data row of a Markdown table."""

    # 1-based line number.
    line: int

    # Cell texts, stripped.
    cells: tuple[str, ...]


@dataclass(frozen=True)
class Table:
    """A Markdown table with a header row and a separator row."""

    # 1-based line number of the header row.
    line: int

    # Header cell texts, stripped.
    header: tuple[str, ...]

    # Data rows.
    rows: tuple[TableRow, ...]


@dataclass(frozen=True)
class DomainSection:
    """A `## UAIP.<...>` section of the reference."""

    # Provider prefix taken from the heading, e.g. `UAIP.Editor.Blueprint`.
    prefix: str

    # 1-based line of the heading.
    line: int

    # First line after the section (exclusive end).
    end_line: int


@dataclass(frozen=True)
class CountHeading:
    """A sub-heading (level 3 or deeper) of a domain section that states a count."""

    # Domain prefix of the section that contains the heading.
    domain: str

    # Heading level.
    level: int

    # Full heading text.
    text: str

    # Heading text without the count, the trailing note and the emoji.
    normalized: str

    # The N stated in the heading.
    count: int

    # 1-based line of the heading.
    line: int

    # First line after the heading's range (exclusive end).
    end_line: int

    # Number of command rows in the range.
    row_count: int

    # Number of command tables in the range (a table with no rows counts).
    command_table_count: int


@dataclass(frozen=True)
class CommandRow:
    """A command row of a command table."""

    # Name as written in the first backtick span of the first column.
    name: str

    # Fully-qualified name (bridge names are used as written).
    full_name: str

    # True when the name starts with `Toolset.`.
    is_bridge: bool

    # True when the first column starts with the demo mark.
    has_demo_mark: bool

    # Domain prefix of the section that contains the row.
    domain: str

    # 1-based line number.
    line: int

    # N of the innermost count heading whose range contains the row, if any.
    innermost_count: int | None


@dataclass(frozen=True)
class SummaryRow:
    """A row of the domain summary table."""

    # Provider prefix from the second column.
    prefix: str

    # Value of the UAIP commands column (a dash is 0).
    native: int

    # Value of the Toolset bridge column (a dash is 0).
    bridge: int

    # Parsed Demo column: ("all",) / ("none",) / ("partial", x, y).
    demo: tuple[object, ...]

    # Demo column as written.
    demo_text: str

    # 1-based line number.
    line: int


@dataclass(frozen=True)
class IntroTotals:
    """The totals in the opening paragraph."""

    # Count of UAIP commands.
    native: int

    # Count of Toolset bridge commands.
    bridge: int

    # Combined total.
    total: int

    # 1-based line that states the totals (the line of the first number found).
    line: int


@dataclass(frozen=True)
class SelectorEntry:
    """One command name of the play-world selector table."""

    # Domain prefix of the table row.
    domain: str

    # Command name.
    name: str

    # 1-based line number.
    line: int


@dataclass(frozen=True)
class SelectorInfo:
    """The play-world selector section."""

    # Number of commands the section says take the selector.
    stated: int

    # 1-based line of the sentence that states the number.
    stated_line: int

    # Names listed in the table, duplicates included.
    entries: tuple[SelectorEntry, ...]


@dataclass(frozen=True)
class DemoConflict:
    """A demo-marked row in a table that follows "not provided in the demo build"."""

    # Domain prefix.
    domain: str

    # Command name.
    name: str

    # 1-based line of the row.
    line: int

    # 1-based line of the sentence.
    phrase_line: int


@dataclass(frozen=True)
class ParsedDocument:
    """The structured content of one language's command reference."""

    # Language code.
    language: str

    # Opening totals.
    intro: IntroTotals

    # Rows of the domain summary.
    summary_rows: tuple[SummaryRow, ...]

    # 1-based line of the domain summary heading.
    summary_line: int

    # Domain sections.
    domain_sections: tuple[DomainSection, ...]

    # Command rows of all domain sections.
    command_rows: tuple[CommandRow, ...]

    # Headings that state a count.
    count_headings: tuple[CountHeading, ...]

    # Play-world selector section.
    selector: SelectorInfo

    # Demo-marked rows that follow a "not provided in the demo build" sentence.
    demo_conflicts: tuple[DemoConflict, ...]


@dataclass(frozen=True)
class ExceptionEntry:
    """One entry of the exception file."""

    # prose-only-bridge or subset-heading.
    kind: str

    # Domain prefix of the section that holds the heading.
    domain: str

    # Normalized English heading.
    heading_en: str

    # Normalized Japanese heading.
    heading_ja: str

    # Why the exception exists.
    reason: str

    # Toolset providers described by the prose (prose-only-bridge only).
    toolset_providers: tuple[str, ...]

    # Command names the heading points at (subset-heading only).
    members: tuple[str, ...]


@dataclass(frozen=True)
class ExceptionSet:
    """The validated exception file."""

    # Upper bound of the number of entries.
    max_entries: int

    # The entries.
    entries: tuple[ExceptionEntry, ...]


@dataclass(frozen=True)
class Finding:
    """One disagreement found by a check."""

    # Check id: K1 to K8, or EXC for the exception file.
    check: str

    # Language of the document the finding is reported against.
    language: str

    # Domain prefix, or None for the whole document.
    domain: str | None

    # 1-based line (0 when there is none).
    line: int

    # The value the document should have had.
    expected: object

    # The value the document has.
    actual: object

    # Human-readable description.
    message: str

    def to_dict(self) -> dict[str, object]:
        """Return the JSON form of the finding."""
        return {
            "check": self.check,
            "language": self.language,
            "domain": self.domain,
            "line": self.line,
            "expected": self.expected,
            "actual": self.actual,
            "message": self.message,
        }


@dataclass(frozen=True)
class ExceptionResolution:
    """How the exception entries apply to one document."""

    # Lines of the headings that an exception handles.
    handled_lines: frozenset[int]

    # Per-domain sum of the counts of the matched prose-only headings.
    prose_counts: dict[str, int]

    # Per-entry count of the matched prose-only heading (index in the entry list).
    entry_counts: dict[int, int]

    # Findings produced while applying the entries.
    findings: tuple[Finding, ...]


@dataclass(frozen=True)
class Evaluation:
    """The outcome of comparing both documents."""

    # All findings, sorted.
    findings: tuple[Finding, ...]

    # Number of items each check looked at.
    reach: dict[str, int]

    # Headings handled by an exception (both languages).
    handled_headings: int

    # Report body (everything except `source` and `verdict`).
    body: dict[str, object]


# --------------------------------------------------------------------------------------
# Reading Markdown
# --------------------------------------------------------------------------------------


def split_table_cells(line: str) -> list[str]:
    """Split a Markdown table row into stripped cells.

    A `|` inside a backtick span or escaped as `\\|` does not split.
    """
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    cells: list[str] = []
    current: list[str] = []
    is_in_code = False
    index = 0
    while index < len(text):
        character = text[index]
        if character == "\\" and index + 1 < len(text) and text[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if character == "`":
            is_in_code = not is_in_code
        if character == "|" and not is_in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
        index += 1
    trailing = "".join(current).strip()
    if trailing:
        cells.append(trailing)
    return cells


def _scan_markdown(text: str) -> tuple[list[str], list[bool], list[Heading], list[Table]]:
    """Return (lines, is_in_fence per line, headings, tables), skipping fences and quotes."""
    lines = text.splitlines()
    fence_flags: list[bool] = []
    headings: list[Heading] = []
    tables: list[Table] = []
    fence_marker: str | None = None
    pending: list[tuple[int, str]] = []

    def flush_pending() -> None:
        """Turn the collected table lines into a Table if they form one."""
        if len(pending) >= 2:
            header = split_table_cells(pending[0][1])
            separator = split_table_cells(pending[1][1])
            if separator and all(_SEPARATOR_CELL_PATTERN.match(cell) for cell in separator):
                rows = tuple(
                    TableRow(line=line_number, cells=tuple(split_table_cells(line_text)))
                    for line_number, line_text in pending[2:]
                )
                tables.append(Table(line=pending[0][0], header=tuple(header), rows=rows))
        pending.clear()

    for index, line_text in enumerate(lines):
        line_number = index + 1
        fence_match = _FENCE_PATTERN.match(line_text)
        if fence_match:
            flush_pending()
            marker = fence_match.group(1)
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            fence_flags.append(True)
            continue
        if fence_marker is not None:
            fence_flags.append(True)
            continue
        fence_flags.append(False)
        if line_text.strip().startswith("|") and not line_text.lstrip().startswith(">"):
            pending.append((line_number, line_text))
            continue
        flush_pending()
        heading_match = _HEADING_PATTERN.match(line_text)
        if heading_match:
            headings.append(Heading(level=len(heading_match.group(1)), text=heading_match.group(2), line=line_number))
    flush_pending()
    return lines, fence_flags, headings, tables


def _range_end(headings: list[Heading], position: int, line_count: int) -> int:
    """Return the first line after the range of headings[position]."""
    level = headings[position].level
    for later_heading in headings[position + 1:]:
        if later_heading.level <= level:
            return later_heading.line
    return line_count + 1


def _first_backtick(text: str) -> str | None:
    """Return the content of the first backtick span, or None."""
    match = _BACKTICK_PATTERN.search(text)
    if match is None:
        return None
    return match.group(1).strip()


def _normalize_title(text: str) -> str:
    """Remove emoji, spaces and trailing dashes from the title part of a heading."""
    cleaned = _DECORATION_PATTERN.sub("", text).strip()
    return re.sub(r"[\s—–-]+$", "", cleaned).strip()


def parse_count_heading(text: str, profile: LanguageProfile) -> tuple[int, str] | None:
    """Return (count, normalized title) of a heading, or None when it states no count.

    A parenthesised group that contains a digit but is not a count in this
    language's notation is an error: a new way of writing counts must not vanish
    from the checks silently.
    """
    masked = _BACKTICK_PATTERN.sub(lambda match: "x" * len(match.group(0)), text)
    valid_groups: list[tuple[int, int]] = []
    for group in _PAREN_GROUP_PATTERN.finditer(masked):
        if _DIGIT_PATTERN.search(group.group(1)) is None:
            continue
        count_match = profile.count_group_pattern.match(group.group(0))
        if count_match is None:
            raise NoVerdictError(
                f"[{profile.code}] heading '{text}' has a parenthesised number '{group.group(0)}' that is not a "
                "count in this language's notation. Write the count in the accepted notation, or extend the "
                "notation table in check_command_counts.py."
            )
        valid_groups.append((group.start(), int(count_match.group(1))))
    if not valid_groups:
        return None
    if len(valid_groups) > 1:
        raise NoVerdictError(f"[{profile.code}] heading '{text}' states more than one count.")
    start, count = valid_groups[0]
    return count, _normalize_title(text[:start])


def _parse_dash_number(text: str, description: str, line: int) -> int:
    """Parse a summary cell: a dash is 0, otherwise an integer."""
    stripped = text.strip()
    if stripped in ("—", "-", "–", ""):
        return 0
    if stripped.isdigit():
        return int(stripped)
    raise NoVerdictError(f"summary table line {line}: {description} '{text}' is neither a number nor a dash.")


def _parse_demo_cell(text: str, line: int) -> tuple[object, ...]:
    """Parse the Demo column of the summary table."""
    stripped = text.strip()
    if stripped == "✅":
        return ("all",)
    if stripped in ("—", "-", "–"):
        return ("none",)
    partial_match = _PARTIAL_DEMO_PATTERN.match(stripped)
    if partial_match:
        return ("partial", int(partial_match.group(1)), int(partial_match.group(2)))
    raise NoVerdictError(f"summary table line {line}: Demo column '{text}' is not understood.")


def _parse_summary(
    tables: list[Table],
    headings: list[Heading],
    profile: LanguageProfile,
    line_count: int,
) -> tuple[tuple[SummaryRow, ...], int]:
    """Return the summary rows and the line of the summary heading."""
    for position, summary_heading in enumerate(headings):
        if summary_heading.level == 2 and summary_heading.text.strip() == profile.summary_heading:
            end_line = _range_end(headings, position, line_count)
            for table in tables:
                if summary_heading.line < table.line < end_line:
                    rows: list[SummaryRow] = []
                    for row in table.rows:
                        if len(row.cells) != 5:
                            raise NoVerdictError(
                                f"[{profile.code}] summary table line {row.line}: expected 5 columns, "
                                f"found {len(row.cells)}."
                            )
                        prefix = _first_backtick(row.cells[1])
                        if prefix is None:
                            raise NoVerdictError(
                                f"[{profile.code}] summary table line {row.line}: no provider prefix in "
                                f"'{row.cells[1]}'."
                            )
                        rows.append(
                            SummaryRow(
                                prefix=prefix,
                                native=_parse_dash_number(row.cells[2], "UAIP commands", row.line),
                                bridge=_parse_dash_number(row.cells[3], "Toolset bridge", row.line),
                                demo=_parse_demo_cell(row.cells[4], row.line),
                                demo_text=row.cells[4],
                                line=row.line,
                            )
                        )
                    return tuple(rows), summary_heading.line
            raise NoVerdictError(f"[{profile.code}] no table follows the '{profile.summary_heading}' heading.")
    raise NoVerdictError(f"[{profile.code}] no '## {profile.summary_heading}' heading.")


def _parse_intro(
    lines: list[str],
    fence_flags: list[bool],
    headings: list[Heading],
    profile: LanguageProfile,
) -> IntroTotals:
    """Read the totals from the paragraphs before the first level-2 heading."""
    first_section = next((heading.line for heading in headings if heading.level == 2), len(lines) + 1)
    found: dict[str, tuple[int, int]] = {}
    patterns = {
        "native": profile.intro_native_pattern,
        "bridge": profile.intro_bridge_pattern,
        "total": profile.intro_total_pattern,
    }
    for index in range(first_section - 1):
        if fence_flags[index]:
            continue
        for name, pattern in patterns.items():
            match = pattern.search(lines[index])
            if match and name not in found:
                found[name] = (int(match.group(1)), index + 1)
    missing = [name for name in patterns if name not in found]
    if missing:
        raise NoVerdictError(f"[{profile.code}] the opening paragraph does not state: {', '.join(missing)}.")
    return IntroTotals(
        native=found["native"][0],
        bridge=found["bridge"][0],
        total=found["total"][0],
        line=min(line for _, line in found.values()),
    )


def _parse_selector(
    lines: list[str],
    fence_flags: list[bool],
    tables: list[Table],
    headings: list[Heading],
    profile: LanguageProfile,
) -> SelectorInfo:
    """Read the play-world selector section."""
    for position, selector_heading in enumerate(headings):
        if selector_heading.level != 2 or selector_heading.text.strip() != profile.selector_heading:
            continue
        end_line = _range_end(headings, position, len(lines))
        stated: tuple[int, int] | None = None
        for index in range(selector_heading.line, end_line - 1):
            if fence_flags[index]:
                continue
            match = profile.selector_stated_pattern.search(lines[index])
            if match:
                stated = (int(match.group(1)), index + 1)
                break
        if stated is None:
            raise NoVerdictError(f"[{profile.code}] the selector section does not state how many commands take it.")
        for table in tables:
            is_selector_table = (
                selector_heading.line < table.line < end_line and
                tuple(table.header[:2]) == profile.selector_table_headers
            )
            if not is_selector_table:
                continue
            entries: list[SelectorEntry] = []
            for row in table.rows:
                domain = (_first_backtick(row.cells[0]) if row.cells else None)
                if domain is None or len(row.cells) < 2:
                    continue
                for name_match in _BACKTICK_PATTERN.finditer(row.cells[1]):
                    entries.append(SelectorEntry(domain=domain, name=name_match.group(1).strip(), line=row.line))
            return SelectorInfo(stated=stated[0], stated_line=stated[1], entries=tuple(entries))
        raise NoVerdictError(f"[{profile.code}] the selector section has no '{profile.selector_table_headers}' table.")
    raise NoVerdictError(f"[{profile.code}] no '## {profile.selector_heading}' heading.")


def parse_document(text: str, language: str) -> ParsedDocument:
    """Parse one command reference into its structured form.

    Raises NoVerdictError when a structure the checks depend on is missing or not understood.
    """
    profile = PROFILES[language]
    lines, fence_flags, headings, tables = _scan_markdown(text)
    line_count = len(lines)

    domain_sections: list[DomainSection] = []
    for position, section_heading in enumerate(headings):
        if section_heading.level != 2:
            continue
        prefix_match = _DOMAIN_PREFIX_PATTERN.match(section_heading.text)
        if prefix_match is None:
            continue
        domain_sections.append(
            DomainSection(
                prefix=prefix_match.group(1),
                line=section_heading.line,
                end_line=_range_end(headings, position, line_count),
            )
        )

    def section_of(line: int) -> DomainSection | None:
        """Return the domain section that contains the line."""
        for section in domain_sections:
            if section.line < line < section.end_line:
                return section
        return None

    command_tables: list[tuple[Table, DomainSection]] = []
    for table in tables:
        section = section_of(table.line)
        if section is None or not table.header:
            continue
        is_command_table = (
            table.header[0] == profile.command_header and
            table.header[-1] == profile.description_header
        )
        if is_command_table:
            command_tables.append((table, section))

    count_headings_raw: list[tuple[Heading, DomainSection, int, str, int]] = []
    for position, candidate in enumerate(headings):
        if candidate.level < 3:
            continue
        section = section_of(candidate.line)
        if section is None:
            continue
        parsed = parse_count_heading(candidate.text, profile)
        if parsed is None:
            continue
        end_line = _range_end(headings, position, line_count)
        count_headings_raw.append((candidate, section, parsed[0], parsed[1], end_line))

    raw_rows: list[tuple[str, str, bool, bool, str, int]] = []
    for table, section in command_tables:
        for row in table.rows:
            if not row.cells:
                continue
            name = _first_backtick(row.cells[0])
            if name is None:
                continue
            is_bridge = name.startswith("Toolset.")
            full_name = (name if is_bridge else f"{section.prefix}.{name}")
            has_demo_mark = row.cells[0].lstrip().startswith("🆓")
            raw_rows.append((name, full_name, is_bridge, has_demo_mark, section.prefix, row.line))

    command_rows: list[CommandRow] = []
    for name, full_name, is_bridge, has_demo_mark, domain, line in raw_rows:
        innermost: tuple[int, int] | None = None
        for candidate, _, count, _, end_line in count_headings_raw:
            if candidate.line < line < end_line and (innermost is None or candidate.line > innermost[0]):
                innermost = (candidate.line, count)
        command_rows.append(
            CommandRow(
                name=name,
                full_name=full_name,
                is_bridge=is_bridge,
                has_demo_mark=has_demo_mark,
                domain=domain,
                line=line,
                innermost_count=(innermost[1] if innermost else None),
            )
        )

    count_headings: list[CountHeading] = []
    for candidate, section, count, normalized, end_line in count_headings_raw:
        count_headings.append(
            CountHeading(
                domain=section.prefix,
                level=candidate.level,
                text=candidate.text,
                normalized=normalized,
                count=count,
                line=candidate.line,
                end_line=end_line,
                row_count=sum(1 for row in command_rows if candidate.line < row.line < end_line),
                command_table_count=sum(
                    1 for table, _ in command_tables if candidate.line < table.line < end_line
                ),
            )
        )

    demo_conflicts: list[DemoConflict] = []
    for section in domain_sections:
        for index in range(section.line, section.end_line - 1):
            line_text = lines[index]
            if fence_flags[index] or line_text.lstrip().startswith(("|", ">")):
                continue
            # Only a sentence that opens its line counts. A phrase in the middle of a
            # paragraph is about named commands ("X is not provided in the demo build;
            # the other seven are"), not about the table that follows.
            if not line_text.strip().startswith(profile.no_demo_phrases):
                continue
            following = next(
                (table for table, owner in command_tables if owner is section and table.line > index + 1),
                None,
            )
            if following is None:
                continue
            for row in following.rows:
                name = (_first_backtick(row.cells[0]) if row.cells else None)
                if name is not None and row.cells[0].lstrip().startswith("🆓"):
                    demo_conflicts.append(
                        DemoConflict(domain=section.prefix, name=name, line=row.line, phrase_line=index + 1)
                    )

    summary_rows, summary_line = _parse_summary(tables, headings, profile, line_count)
    return ParsedDocument(
        language=language,
        intro=_parse_intro(lines, fence_flags, headings, profile),
        summary_rows=summary_rows,
        summary_line=summary_line,
        domain_sections=tuple(domain_sections),
        command_rows=tuple(command_rows),
        count_headings=tuple(count_headings),
        selector=_parse_selector(lines, fence_flags, tables, headings, profile),
        demo_conflicts=tuple(demo_conflicts),
    )


# --------------------------------------------------------------------------------------
# Exception file
# --------------------------------------------------------------------------------------


def _is_integer(value: object) -> bool:
    """Return True for an int that is not a bool."""
    return isinstance(value, int) and not isinstance(value, bool)


def _require_string(value: object, description: str) -> str:
    """Return a non-empty string or raise NoVerdictError."""
    if not isinstance(value, str) or not value.strip():
        raise NoVerdictError(f"exception file: {description} must be a non-empty string.")
    return value


def _require_string_list(value: object, description: str) -> tuple[str, ...]:
    """Return a non-empty tuple of non-empty strings or raise NoVerdictError."""
    if not isinstance(value, list) or not value:
        raise NoVerdictError(f"exception file: {description} must be a non-empty array of strings.")
    return tuple(_require_string(item, f"{description}[]") for item in value)


def parse_exceptions(text: str) -> ExceptionSet:
    """Validate the exception file and return it.

    Every malformed shape ends the run with exit code 2: a misspelled key must
    not make an entry silently inactive.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise NoVerdictError(f"exception file: not valid JSON ({error}).") from error
    if not isinstance(data, dict):
        raise NoVerdictError("exception file: the top level must be an object.")
    unknown_top = set(data) - {"schema_version", "max_entries", "exceptions"}
    if unknown_top:
        raise NoVerdictError(f"exception file: unknown top-level keys {sorted(unknown_top)}.")
    for required in ("schema_version", "max_entries", "exceptions"):
        if required not in data:
            raise NoVerdictError(f"exception file: missing '{required}'.")
    if not _is_integer(data["schema_version"]) or data["schema_version"] != EXCEPTIONS_SCHEMA_VERSION:
        raise NoVerdictError(f"exception file: schema_version must be {EXCEPTIONS_SCHEMA_VERSION}.")
    if not _is_integer(data["max_entries"]) or data["max_entries"] < 0:
        raise NoVerdictError("exception file: max_entries must be a non-negative integer.")
    if not isinstance(data["exceptions"], list):
        raise NoVerdictError("exception file: 'exceptions' must be an array.")

    entries: list[ExceptionEntry] = []
    seen_providers: set[str] = set()
    seen_keys: set[tuple[str, str, str]] = set()
    for position, raw in enumerate(data["exceptions"]):
        where = f"exceptions[{position}]"
        if not isinstance(raw, dict):
            raise NoVerdictError(f"exception file: {where} must be an object.")
        kind = raw.get("kind")
        if kind not in EXCEPTION_KINDS:
            raise NoVerdictError(f"exception file: {where}.kind must be one of {list(EXCEPTION_KINDS)}.")
        kind_keys = ("toolset_providers" if kind == KIND_PROSE_ONLY_BRIDGE else "members")
        allowed = {"kind", "domain", "heading", "reason", kind_keys}
        unknown = set(raw) - allowed
        if unknown:
            raise NoVerdictError(f"exception file: {where} has unknown keys {sorted(unknown)}.")
        for required in sorted(allowed):
            if required not in raw:
                raise NoVerdictError(f"exception file: {where} is missing '{required}'.")
        domain = _require_string(raw["domain"], f"{where}.domain")
        reason = _require_string(raw["reason"], f"{where}.reason")
        heading = raw["heading"]
        if not isinstance(heading, dict) or set(heading) != {"en", "ja"}:
            raise NoVerdictError(f"exception file: {where}.heading must be an object with exactly 'en' and 'ja'.")
        heading_en = _require_string(heading["en"], f"{where}.heading.en").strip()
        heading_ja = _require_string(heading["ja"], f"{where}.heading.ja").strip()
        providers: tuple[str, ...] = ()
        members: tuple[str, ...] = ()
        if kind == KIND_PROSE_ONLY_BRIDGE:
            providers = _require_string_list(raw["toolset_providers"], f"{where}.toolset_providers")
            for provider in providers:
                if not provider.startswith("Toolset."):
                    raise NoVerdictError(f"exception file: {where}: provider '{provider}' must start with 'Toolset.'.")
                if provider in seen_providers:
                    raise NoVerdictError(
                        f"exception file: provider '{provider}' appears in more than one entry or twice in one."
                    )
                seen_providers.add(provider)
        else:
            members = _require_string_list(raw["members"], f"{where}.members")
        for language_code, heading_text in (("en", heading_en), ("ja", heading_ja)):
            key = (domain, language_code, heading_text)
            if key in seen_keys:
                raise NoVerdictError(f"exception file: {where} repeats the heading key {key}.")
            seen_keys.add(key)
        entries.append(
            ExceptionEntry(
                kind=kind,
                domain=domain,
                heading_en=heading_en,
                heading_ja=heading_ja,
                reason=reason,
                toolset_providers=providers,
                members=members,
            )
        )
    return ExceptionSet(max_entries=data["max_entries"], entries=tuple(entries))


def resolve_exceptions(document: ParsedDocument, exception_set: ExceptionSet) -> ExceptionResolution:
    """Apply the exception entries to one document.

    An entry must match exactly one heading: none means it is stale (a finding),
    more than one is ambiguous (no verdict).
    """
    handled: set[int] = set()
    prose_counts: dict[str, int] = {}
    entry_counts: dict[int, int] = {}
    findings: list[Finding] = []
    domain_names: dict[str, set[str]] = {}
    for row in document.command_rows:
        domain_names.setdefault(row.domain, set()).add(row.name)

    for position, entry in enumerate(exception_set.entries):
        heading_text = (entry.heading_en if document.language == "en" else entry.heading_ja)
        matches = [
            candidate
            for candidate in document.count_headings
            if candidate.domain == entry.domain and candidate.normalized == heading_text
        ]
        if len(matches) > 1:
            raise NoVerdictError(
                f"[{document.language}] exception '{entry.domain}' / '{heading_text}' matches "
                f"{len(matches)} headings (lines {[match.line for match in matches]}); it must match exactly one."
            )
        if not matches:
            findings.append(
                Finding(
                    check="EXC",
                    language=document.language,
                    domain=entry.domain,
                    line=0,
                    expected=1,
                    actual=0,
                    message=(
                        f"stale exception ({entry.kind}): no heading '{heading_text}' with a count in {entry.domain}. "
                        "Remove the entry or fix the heading."
                    ),
                )
            )
            continue
        matched = matches[0]
        if entry.kind == KIND_PROSE_ONLY_BRIDGE:
            if matched.row_count > 0:
                findings.append(
                    Finding(
                        check="EXC",
                        language=document.language,
                        domain=entry.domain,
                        line=matched.line,
                        expected=0,
                        actual=matched.row_count,
                        message=(
                            f"stale exception (prose-only-bridge): '{matched.text}' now lists {matched.row_count} "
                            "command rows, so it no longer needs the exception. Remove the entry."
                        ),
                    )
                )
                continue
            prose_counts[entry.domain] = prose_counts.get(entry.domain, 0) + matched.count
            entry_counts[position] = matched.count
            handled.add(matched.line)
            continue
        if matched.command_table_count > 0:
            findings.append(
                Finding(
                    check="EXC",
                    language=document.language,
                    domain=entry.domain,
                    line=matched.line,
                    expected=0,
                    actual=matched.command_table_count,
                    message=(
                        f"stale exception (subset-heading): '{matched.text}' now has its own command table. "
                        "Remove the entry."
                    ),
                )
            )
            continue
        if len(entry.members) != matched.count:
            findings.append(
                Finding(
                    check="K3",
                    language=document.language,
                    domain=entry.domain,
                    line=matched.line,
                    expected=matched.count,
                    actual=len(entry.members),
                    message=(
                        f"'{matched.text}' states {matched.count} but the exception lists {len(entry.members)} members."
                    ),
                )
            )
        known_names = domain_names.get(entry.domain, set())
        for member in entry.members:
            if member not in known_names:
                findings.append(
                    Finding(
                        check="K3",
                        language=document.language,
                        domain=entry.domain,
                        line=matched.line,
                        expected=member,
                        actual=None,
                        message=f"'{matched.text}': member '{member}' is not a command row of {entry.domain}.",
                    )
                )
        handled.add(matched.line)
    return ExceptionResolution(
        handled_lines=frozenset(handled),
        prose_counts=prose_counts,
        entry_counts=entry_counts,
        findings=tuple(findings),
    )


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------


def _expected_demo_text(native: int, demo_count: int) -> str:
    """Return the Demo column text a summary row should have."""
    if native == 0 or demo_count == 0:
        return "—"
    if demo_count == native:
        return "✅"
    return f"partial ({demo_count}/{native})"


def _is_demo_cell_correct(row: SummaryRow, demo_count: int) -> bool:
    """Return True when the Demo column agrees with the counted demo marks."""
    kind = row.demo[0]
    if kind == "all":
        return row.native > 0 and demo_count == row.native
    if kind == "none":
        return demo_count == 0
    partial_count = row.demo[1]
    total_count = row.demo[2]
    return (
        isinstance(partial_count, int) and
        isinstance(total_count, int) and
        0 < partial_count < total_count and
        partial_count == demo_count and
        total_count == row.native
    )


def check_document(
    document: ParsedDocument,
    resolution: ExceptionResolution,
    reach: dict[str, int],
) -> list[Finding]:
    """Run K1 to K4, K6, K7 and K8 on one document. `reach` receives the number of items seen."""
    language = document.language
    findings: list[Finding] = list(resolution.findings)

    def add(check: str, domain: str | None, line: int, expected: object, actual: object, message: str) -> None:
        """Append a finding for this document."""
        findings.append(Finding(check, language, domain, line, expected, actual, message))

    def count(check: str, amount: int = 1) -> None:
        """Add to the number of items a check has seen."""
        reach[check] = reach.get(check, 0) + amount

    prose_total = sum(resolution.prose_counts.values())
    native_rows = [row for row in document.command_rows if not row.is_bridge]
    bridge_rows = [row for row in document.command_rows if row.is_bridge]

    # K1: opening totals = summary totals = listed commands.
    summary_native = sum(row.native for row in document.summary_rows)
    summary_bridge = sum(row.bridge for row in document.summary_rows)
    quantities = (
        ("native", document.intro.native, summary_native, len(native_rows)),
        ("bridge", document.intro.bridge, summary_bridge, len(bridge_rows) + prose_total),
        (
            "total",
            document.intro.total,
            summary_native + summary_bridge,
            len(native_rows) + len(bridge_rows) + prose_total,
        ),
    )
    for name, intro_value, summary_value, listed_value in quantities:
        count("K1", 2)
        if intro_value != summary_value:
            add(
                "K1", None, document.intro.line, summary_value, intro_value,
                f"the opening paragraph states {intro_value} {name} commands but the summary table adds up to "
                f"{summary_value}.",
            )
        if summary_value != listed_value:
            add(
                "K1", None, document.summary_line, listed_value, summary_value,
                f"the summary table adds up to {summary_value} {name} commands but {listed_value} are listed "
                "(command rows plus prose-only bridge counts).",
            )
    count("K1")
    if document.intro.total != document.intro.native + document.intro.bridge:
        add(
            "K1", None, document.intro.line, document.intro.native + document.intro.bridge, document.intro.total,
            f"the opening total {document.intro.total} is not {document.intro.native} + {document.intro.bridge}.",
        )

    # K2: each summary row = the commands of its section, in both directions.
    summary_by_prefix: dict[str, SummaryRow] = {}
    for row in document.summary_rows:
        count("K2")
        if row.prefix in summary_by_prefix:
            add("K2", row.prefix, row.line, None, row.prefix, f"summary prefix {row.prefix} appears more than once.")
            continue
        summary_by_prefix[row.prefix] = row
    toolset_prefixes = sorted((prefix for prefix in summary_by_prefix if prefix.startswith("Toolset.")), key=len)
    native_actual: dict[str, int] = {}
    bridge_actual: dict[str, int] = {}
    demo_actual: dict[str, int] = {}
    for row in document.command_rows:
        if row.is_bridge:
            owner = row.domain
            for toolset_prefix in toolset_prefixes:
                if row.full_name.startswith(toolset_prefix + "."):
                    owner = toolset_prefix
            bridge_actual[owner] = bridge_actual.get(owner, 0) + 1
        else:
            native_actual[row.domain] = native_actual.get(row.domain, 0) + 1
            if row.has_demo_mark:
                demo_actual[row.domain] = demo_actual.get(row.domain, 0) + 1
    for domain, prose_count in resolution.prose_counts.items():
        bridge_actual[domain] = bridge_actual.get(domain, 0) + prose_count
    for prefix, row in summary_by_prefix.items():
        actual_native = native_actual.get(prefix, 0)
        actual_bridge = bridge_actual.get(prefix, 0)
        if row.native != actual_native:
            add(
                "K2", prefix, row.line, row.native, actual_native,
                f"summary row {prefix}: UAIP commands is {row.native} but the section lists {actual_native}.",
            )
        if row.bridge != actual_bridge:
            add(
                "K2", prefix, row.line, row.bridge, actual_bridge,
                f"summary row {prefix}: Toolset bridge is {row.bridge} but {actual_bridge} are listed "
                "(rows plus prose-only count).",
            )
    section_lines = {section.prefix: section.line for section in document.domain_sections}
    domains_with_commands = sorted(set(native_actual) | set(bridge_actual) | set(demo_actual))
    for domain in domains_with_commands:
        if domain.startswith("Toolset."):
            continue
        count("K2")
        has_content = native_actual.get(domain, 0) > 0 or bridge_actual.get(domain, 0) > 0
        if has_content and domain not in summary_by_prefix:
            add(
                "K2", domain, section_lines.get(domain, 0), None, domain,
                f"section {domain} lists commands but has no row in the summary table.",
            )

    # K3 / K4: counts in sub-headings.
    for heading in document.count_headings:
        if heading.line in resolution.handled_lines:
            continue
        count("K3")
        count("K4")
        if heading.row_count == 0:
            reason = (
                "has no command table"
                if heading.command_table_count == 0
                else "has a command table with no command rows"
            )
            add(
                "K4", heading.domain, heading.line, heading.count, 0,
                f"'{heading.text}' states {heading.count} but its range {reason}.",
            )
        elif heading.count != heading.row_count:
            add(
                "K3", heading.domain, heading.line, heading.count, heading.row_count,
                f"'{heading.text}' states {heading.count} but its range lists {heading.row_count} command rows.",
            )

    # K6: the selector count.
    selector = document.selector
    count("K6", 1 + len(selector.entries))
    if selector.stated != len(selector.entries):
        add(
            "K6", None, selector.stated_line, selector.stated, len(selector.entries),
            f"the selector section states {selector.stated} commands but its table lists {len(selector.entries)}.",
        )
    seen_entries: dict[tuple[str, str], int] = {}
    names_by_domain: dict[str, set[str]] = {}
    for row in document.command_rows:
        names_by_domain.setdefault(row.domain, set()).add(row.name)
    for entry in selector.entries:
        key = (entry.domain, entry.name)
        if key in seen_entries:
            add(
                "K6", entry.domain, entry.line, 1, 2,
                f"selector table lists {entry.domain} {entry.name} twice (first at line {seen_entries[key]}).",
            )
        else:
            seen_entries[key] = entry.line
        if entry.name not in names_by_domain.get(entry.domain, set()):
            add(
                "K6", entry.domain, entry.line, entry.name, None,
                f"selector table lists {entry.name} under {entry.domain} but that section has no such command row.",
            )

    # K7: the Demo column.
    for row in document.summary_rows:
        count("K7")
        demo_count = demo_actual.get(row.prefix, 0)
        if not _is_demo_cell_correct(row, demo_count):
            add(
                "K7", row.prefix, row.line, _expected_demo_text(row.native, demo_count), row.demo_text,
                f"summary row {row.prefix}: Demo column is '{row.demo_text}' but the section marks {demo_count} of "
                f"{row.native} UAIP commands as available in the demo.",
            )
    for conflict in document.demo_conflicts:
        count("K7")
        add(
            "K7", conflict.domain, conflict.line, False, True,
            f"{conflict.name} has the demo mark but the sentence at line {conflict.phrase_line} says the commands "
            "are not provided in the demo build.",
        )

    # K8: a name is listed once.
    first_lines: dict[str, int] = {}
    for row in document.command_rows:
        count("K8")
        if row.full_name in first_lines:
            add(
                "K8", row.domain, row.line, 1, 2,
                f"{row.full_name} is listed twice (first at line {first_lines[row.full_name]}).",
            )
        else:
            first_lines[row.full_name] = row.line
    return findings


def check_across_languages(
    english: ParsedDocument,
    japanese: ParsedDocument,
    reach: dict[str, int],
) -> list[Finding]:
    """Run K5: the English and the Japanese document state the same values."""
    findings: list[Finding] = []

    def add(domain: str | None, line: int, expected: object, actual: object, message: str) -> None:
        """Append a K5 finding (reported against the English side)."""
        findings.append(Finding("K5", "en", domain, line, expected, actual, message))

    reach["K5"] = reach.get("K5", 0)

    for name in ("native", "bridge", "total"):
        reach["K5"] += 1
        english_value = getattr(english.intro, name)
        japanese_value = getattr(japanese.intro, name)
        if english_value != japanese_value:
            add(
                None,
                english.intro.line,
                english_value,
                japanese_value,
                f"opening {name} total: en {english_value}, ja {japanese_value}.",
            )

    english_summary = {row.prefix: row for row in english.summary_rows}
    japanese_summary = {row.prefix: row for row in japanese.summary_rows}
    for prefix in sorted(set(english_summary) | set(japanese_summary)):
        reach["K5"] += 1
        english_row = english_summary.get(prefix)
        japanese_row = japanese_summary.get(prefix)
        if english_row is None or japanese_row is None:
            present = ("en" if english_row else "ja")
            add(
                prefix,
                (english_row or japanese_row).line,
                present,
                None,
                f"summary row {prefix} exists only in {present}.",
            )
            continue
        for field_name in ("native", "bridge", "demo"):
            english_value = getattr(english_row, field_name)
            japanese_value = getattr(japanese_row, field_name)
            if english_value != japanese_value:
                add(
                    prefix, english_row.line, english_value, japanese_value,
                    f"summary row {prefix} {field_name}: en {english_value}, ja {japanese_value}.",
                )

    def names_by_domain(document: ParsedDocument, only_demo: bool) -> dict[str, set[str]]:
        """Collect the fully-qualified names per domain section."""
        result: dict[str, set[str]] = {}
        for row in document.command_rows:
            if only_demo and not (row.has_demo_mark and not row.is_bridge):
                continue
            result.setdefault(row.domain, set()).add(row.full_name)
        return result

    section_lines = {section.prefix: section.line for section in english.domain_sections}
    for label, only_demo in (("commands", False), ("demo-marked commands", True)):
        english_names = names_by_domain(english, only_demo)
        japanese_names = names_by_domain(japanese, only_demo)
        for domain in sorted(set(english_names) | set(japanese_names)):
            reach["K5"] += 1
            only_english = sorted(english_names.get(domain, set()) - japanese_names.get(domain, set()))
            only_japanese = sorted(japanese_names.get(domain, set()) - english_names.get(domain, set()))
            if only_english or only_japanese:
                add(
                    domain, section_lines.get(domain, 0), only_english, only_japanese,
                    f"{domain} {label} differ: only in en {only_english}, only in ja {only_japanese}.",
                )

    reach["K5"] += 1
    if english.selector.stated != japanese.selector.stated:
        add(
            None, english.selector.stated_line, english.selector.stated, japanese.selector.stated,
            f"selector count: en {english.selector.stated}, ja {japanese.selector.stated}.",
        )
    english_entries = {(entry.domain, entry.name) for entry in english.selector.entries}
    japanese_entries = {(entry.domain, entry.name) for entry in japanese.selector.entries}
    reach["K5"] += 1
    if english_entries != japanese_entries:
        only_english_entries = sorted(f"{domain} {name}" for domain, name in english_entries - japanese_entries)
        only_japanese_entries = sorted(f"{domain} {name}" for domain, name in japanese_entries - english_entries)
        add(
            None, english.selector.stated_line, only_english_entries, only_japanese_entries,
            f"selector table names differ: only in en {only_english_entries}, only in ja {only_japanese_entries}.",
        )

    english_rows = {row.full_name: row for row in reversed(english.command_rows)}
    japanese_rows = {row.full_name: row for row in reversed(japanese.command_rows)}
    for full_name in sorted(set(english_rows) & set(japanese_rows)):
        reach["K5"] += 1
        english_count = english_rows[full_name].innermost_count
        japanese_count = japanese_rows[full_name].innermost_count
        if english_count != japanese_count:
            add(
                english_rows[full_name].domain, english_rows[full_name].line, english_count, japanese_count,
                f"{full_name} sits under a heading with count {english_count} in en but {japanese_count} in ja.",
            )
    return findings


def evaluate_documents(
    english: ParsedDocument,
    japanese: ParsedDocument,
    exception_set: ExceptionSet,
) -> Evaluation:
    """Run every check on a pair of parsed documents."""
    reach: dict[str, int] = {}
    english_resolution = resolve_exceptions(english, exception_set)
    japanese_resolution = resolve_exceptions(japanese, exception_set)
    findings: list[Finding] = []
    findings.extend(check_document(english, english_resolution, reach))
    findings.extend(check_document(japanese, japanese_resolution, reach))
    findings.extend(check_across_languages(english, japanese, reach))

    reach["EXC"] = len(exception_set.entries)
    if len(exception_set.entries) > exception_set.max_entries:
        findings.append(
            Finding(
                check="EXC",
                language="en",
                domain=None,
                line=0,
                expected=exception_set.max_entries,
                actual=len(exception_set.entries),
                message=(
                    f"the exception file has {len(exception_set.entries)} entries, more than max_entries "
                    f"({exception_set.max_entries}). Fix the documents instead of adding exceptions."
                ),
            )
        )

    headings_checked = len(english.count_headings) + len(japanese.count_headings)
    handled_headings = len(english_resolution.handled_lines) + len(japanese_resolution.handled_lines)
    if not english.domain_sections or not english.command_rows or not japanese.command_rows or headings_checked == 0:
        raise NoVerdictError(
            "the documents have no domain sections, command rows or counted headings; nothing was checked."
        )

    sorted_findings = tuple(sorted(findings, key=lambda finding: (finding.language, finding.line, finding.check)))
    body = _build_body(english, japanese, exception_set, english_resolution, japanese_resolution, headings_checked)
    return Evaluation(findings=sorted_findings, reach=reach, handled_headings=handled_headings, body=body)


def _build_body(
    english: ParsedDocument,
    japanese: ParsedDocument,
    exception_set: ExceptionSet,
    english_resolution: ExceptionResolution,
    japanese_resolution: ExceptionResolution,
    headings_checked: int,
) -> dict[str, object]:
    """Build the data part of the JSON report."""

    def unique_names(document: ParsedDocument, is_bridge: bool) -> list[str]:
        """Return the sorted fully-qualified names without duplicates."""
        return sorted({row.full_name for row in document.command_rows if row.is_bridge == is_bridge})

    prose_only: list[dict[str, object]] = []
    for position, entry in enumerate(exception_set.entries):
        if entry.kind != KIND_PROSE_ONLY_BRIDGE:
            continue
        prose_only.append(
            {
                "domain": entry.domain,
                "count": {
                    "en": english_resolution.entry_counts.get(position, 0),
                    "ja": japanese_resolution.entry_counts.get(position, 0),
                },
                "toolset_providers": list(entry.toolset_providers),
            }
        )
    return {
        "selector": {
            "en": {"stated": english.selector.stated, "listed": len(english.selector.entries)},
            "ja": {"stated": japanese.selector.stated, "listed": len(japanese.selector.entries)},
        },
        "native_names": {"en": unique_names(english, False), "ja": unique_names(japanese, False)},
        "bridge": {
            "listed_names": {"en": unique_names(english, True), "ja": unique_names(japanese, True)},
            "prose_only": prose_only,
            "summary_total": sum(row.bridge for row in english.summary_rows),
        },
        "reach": {
            "domain_sections": len(english.domain_sections),
            "command_rows": {"en": len(english.command_rows), "ja": len(japanese.command_rows)},
            "headings_checked": headings_checked,
            "exceptions": len(exception_set.entries),
        },
    }


def build_report(source: dict[str, object], evaluation: Evaluation) -> dict[str, object]:
    """Build the JSON report of a run that reached a verdict."""
    report: dict[str, object] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "source": source,
        "verdict": ("inconsistent" if evaluation.findings else "consistent"),
        "findings": [finding.to_dict() for finding in evaluation.findings],
    }
    report.update(evaluation.body)
    return report


def build_no_verdict_report(source: dict[str, object], reason: str) -> dict[str, object]:
    """Build the JSON report of a run that could not reach a verdict."""
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "source": source,
        "verdict": "no-verdict",
        "findings": [],
        "no_verdict_reason": reason,
        "selector": {"en": {"stated": 0, "listed": 0}, "ja": {"stated": 0, "listed": 0}},
        "native_names": {"en": [], "ja": []},
        "bridge": {"listed_names": {"en": [], "ja": []}, "prose_only": [], "summary_total": 0},
        "reach": {
            "domain_sections": 0,
            "command_rows": {"en": 0, "ja": 0},
            "headings_checked": 0,
            "exceptions": 0,
        },
    }


def check_texts(
    english_text: str,
    japanese_text: str,
    exceptions_text: str,
    source: dict[str, object],
) -> tuple[Evaluation, dict[str, object]]:
    """Parse the texts, run the checks and return the evaluation with its JSON report.

    Raises NoVerdictError when no verdict can be reached.
    """
    exception_set = parse_exceptions(exceptions_text)
    english = parse_document(english_text, "en")
    japanese = parse_document(japanese_text, "ja")
    evaluation = evaluate_documents(english, japanese, exception_set)
    return evaluation, build_report(source, evaluation)


# --------------------------------------------------------------------------------------
# Input and command line
# --------------------------------------------------------------------------------------


def _decode(data: bytes, description: str) -> str:
    """Decode UTF-8 (with or without a BOM)."""
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise NoVerdictError(f"{description} is not valid UTF-8 ({error}).") from error


def run_git(arguments: list[str], repository_root: str | None) -> bytes:
    """Run git with an argument array (no shell) and return its standard output."""
    command = ["git"]
    if repository_root is not None:
        command += ["-C", repository_root]
    command += arguments
    environment = {
        key: value for key, value in os.environ.items() if key not in SCRUBBED_ENVIRONMENT_VARIABLES
    }
    try:
        completed = subprocess.run(command, capture_output=True, check=False, shell=False, env=environment)
    except OSError as error:
        raise NoVerdictError(f"cannot run git: {error}") from error
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise NoVerdictError(f"git {' '.join(arguments)} failed: {detail}")
    return completed.stdout


def _read_file(path: str, description: str) -> str:
    """Read a UTF-8 file."""
    try:
        return _decode(Path(path).read_bytes(), description)
    except OSError as error:
        raise NoVerdictError(f"cannot read {description} '{path}': {error}") from error


def load_inputs(arguments: argparse.Namespace) -> tuple[str, str, str, dict[str, object]]:
    """Return (English text, Japanese text, exception file text, source) for the chosen mode."""
    if arguments.en is not None:
        # Direct files: no git command is run and no repository root is needed.
        english_text = _read_file(arguments.en, "English document")
        japanese_text = _read_file(arguments.ja, "Japanese document")
        exceptions_text = _read_file(arguments.exceptions, "exception file")
        return english_text, japanese_text, exceptions_text, {"mode": "files"}

    root = _decode(run_git(["rev-parse", "--show-toplevel"], None), "repository root").strip()
    source: dict[str, object]
    if arguments.rev is not None:
        sha = _decode(run_git(["rev-parse", "--verify", arguments.rev + "^{commit}"], root), "revision").strip()
        source = {"mode": "rev", "rev": sha}

        def read_repository_file(path: str) -> str:
            """Read a file as it is at the revision."""
            return _decode(run_git(["show", f"{sha}:{path}"], root), path)
    elif arguments.worktree:
        source = {"mode": "worktree"}

        def read_repository_file(path: str) -> str:
            """Read a file from the working tree."""
            return _read_file(str(Path(root) / path), path)
    else:
        source = {"mode": "index"}

        def read_repository_file(path: str) -> str:
            """Read a file as it is staged."""
            return _decode(run_git(["show", f":{path}"], root), path)

    english_text = read_repository_file(ENGLISH_DOCUMENT_PATH)
    japanese_text = read_repository_file(JAPANESE_DOCUMENT_PATH)
    if arguments.exceptions is not None:
        exceptions_text = _read_file(arguments.exceptions, "exception file")
    else:
        exceptions_text = read_repository_file(EXCEPTIONS_PATH)
    return english_text, japanese_text, exceptions_text, source


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        description="Check the counts in docs/{en,ja}/commands.md against the commands they list.",
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--rev", help="read the documents at this commit")
    modes.add_argument("--worktree", action="store_true", help="read the working tree files")
    modes.add_argument("--en", help="English document (use with --ja and --exceptions; runs no git command)")
    parser.add_argument("--ja", help="Japanese document (use with --en)")
    parser.add_argument("--exceptions", help="exception file (required with --en/--ja)")
    parser.add_argument("--json", action="store_true", help="write a JSON report to stdout; text goes to stderr")
    return parser


def format_text_report(evaluation: Evaluation) -> list[str]:
    """Return the human-readable lines of a run that reached a verdict."""
    lines: list[str] = []
    descriptions = {
        "K1": "totals (opening / summary / listed)",
        "K2": "summary rows and domain sections",
        "K3": "sub-heading counts",
        "K4": "sub-headings with a command table",
        "K5": "en / ja agreement",
        "K6": "play-world selector",
        "K7": "Demo column",
        "K8": "duplicate command names",
        "EXC": "exception entries",
    }
    for check, description in descriptions.items():
        seen = evaluation.reach.get(check, 0)
        failures = sum(1 for finding in evaluation.findings if finding.check == check)
        status = ("OK" if failures == 0 else f"{failures} finding(s)")
        lines.append(f"{check} {description}: looked at {seen} items, {status}")
    reach = evaluation.body["reach"]
    assert isinstance(reach, dict)
    lines.append(
        f"Reach: {reach['domain_sections']} domain sections, command rows {reach['command_rows']}, "
        f"{reach['headings_checked']} headings checked (en + ja), {evaluation.handled_headings} handled by exceptions."
    )
    for finding in evaluation.findings:
        location = (f"{finding.language} line {finding.line}" if finding.line else finding.language)
        lines.append(f"  [{finding.check}] {location}: {finding.message}")
    return lines


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns 0 (consistent), 1 (inconsistent) or 2 (no verdict)."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = build_argument_parser()
    try:
        arguments = parser.parse_args(argv)
    except SystemExit as exit_request:
        return (exit_request.code if isinstance(exit_request.code, int) else 2)

    text_stream = (sys.stderr if arguments.json else sys.stdout)
    source: dict[str, object] = {"mode": "unknown"}
    try:
        if (arguments.en is None) != (arguments.ja is None):
            raise NoVerdictError("--en and --ja must be given together.")
        if arguments.en is not None and arguments.exceptions is None:
            raise NoVerdictError("--exceptions is required with --en/--ja.")
        english_text, japanese_text, exceptions_text, source = load_inputs(arguments)
        evaluation, report = check_texts(english_text, japanese_text, exceptions_text, source)
    except NoVerdictError as error:
        print(f"check_command_counts: no verdict: {error}", file=text_stream)
        if arguments.json:
            print(json.dumps(build_no_verdict_report(source, str(error)), ensure_ascii=True, indent=2))
        return 2

    for line in format_text_report(evaluation):
        print(line, file=text_stream)
    if arguments.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    if evaluation.findings:
        message = f"check_command_counts: INCONSISTENT ({len(evaluation.findings)} finding(s)). {FIX_HINT}"
        print(message, file=text_stream)
        return 1
    print("check_command_counts: consistent.", file=text_stream)
    return 0


if __name__ == "__main__":
    sys.exit(main())
