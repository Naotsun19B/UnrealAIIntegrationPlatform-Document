#!/usr/bin/env python3
"""Contrast tests for check_command_counts.py.

Every check (K1 to K8) is shown to fire on a document that is wrong in exactly
that way and to stay quiet on a document that is right. The documents are small
synthetic Markdown files built here; a few of them are cut down from the
mistakes that the real command reference had at commit 806ce0f8.

Run with:  python -I -m unittest discover -s docs/scripts -p "test_*.py"
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Final
from unittest import mock

# `python -I` does not put the script's directory on sys.path, so add it before the import below.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_command_counts as counts  # noqa: E402

# Directory that holds this test and the script under test.
SCRIPT_DIRECTORY: Final = Path(__file__).resolve().parent

# The two synthetic domains of the baseline document.
ALPHA: Final = "UAIP.Editor.Alpha"
BETA: Final = "UAIP.Editor.Beta"

# Summary table rows of the baseline document: (prefix, UAIP commands, Toolset bridge, Demo).
BASE_SUMMARY: Final = ((ALPHA, 3, 2, "partial (1/3)"), (BETA, 2, 4, "—"))

# The baseline summary row of ALPHA as it is written in both languages.
ALPHA_SUMMARY_ROW: Final = "| Editor | `UAIP.Editor.Alpha` | 3 | 2 | partial (1/3) |"

# The baseline summary row of BETA as it is written in both languages.
BETA_SUMMARY_ROW: Final = "| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |"

# Heading texts of the baseline document per language.
HEADING_TEXT: Final = {
    "en": {
        "section_a": "Section A",
        "section_b": "Section B",
        "bridges": "Bridges",
        "main": "Main",
        "subset": "Subset note",
        "prose": "Toolset bridges",
    },
    "ja": {
        "section_a": "セクション A",
        "section_b": "セクション B",
        "bridges": "ブリッジ",
        "main": "メイン",
        "subset": "サブセット注記",
        "prose": "Toolset ブリッジ",
    },
}

# Every check id the report counts.
ALL_CHECKS: Final = ("K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "EXC")

# Keys of one finding in the JSON report.
FINDING_KEYS: Final = {"check", "language", "domain", "line", "expected", "actual", "message"}

# Keys of the JSON report that every run has.
REPORT_KEYS: Final = {
    "schema_version",
    "source",
    "verdict",
    "findings",
    "selector",
    "native_names",
    "bridge",
    "reach",
}

# The number of exception entries the real exception file may hold (a reviewed limit).
EXPECTED_MAX_ENTRIES: Final = 10


# --------------------------------------------------------------------------------------
# Building documents
# --------------------------------------------------------------------------------------


def count_label(language: str, number: int) -> str:
    """Return the count notation of a heading in the given language."""
    return (f" ({number})" if language == "en" else f"（{number}）")


def heading(language: str, key: str, number: int | None = None, level: int = 3) -> str:
    """Return a Markdown heading line of the baseline document."""
    marks = "#" * level
    text = HEADING_TEXT[language][key]
    if number is not None:
        text += count_label(language, number)
    return f"{marks} {text}"


def table_markdown(language: str, first_cells: Sequence[str]) -> str:
    """Return a command table whose rows have the given first cells."""
    command_header = ("Command" if language == "en" else "コマンド")
    description_header = ("Description" if language == "en" else "説明")
    lines = [f"| {command_header} | {description_header} |", "|---|---|"]
    lines.extend(f"| {cell} | desc |" for cell in first_cells)
    return "\n".join(lines)


def domain_block(
    language: str,
    prefix: str,
    sub_heading: str,
    names: Sequence[str],
    marked_count: int = 0,
) -> str:
    """Return a domain section with one sub-heading and one command table."""
    cells = [(f"🆓 `{name}`" if index < marked_count else f"`{name}`") for index, name in enumerate(names)]
    return "\n".join([f"## {prefix}", "", sub_heading, "", table_markdown(language, cells), ""])


def render_document(
    language: str,
    summary_rows: Sequence[tuple[str, int, int, str]],
    body: str,
    selector_entries: Sequence[tuple[str, str]] = (),
) -> str:
    """Render a whole command reference whose opening totals agree with its summary table."""
    native = sum(row[1] for row in summary_rows)
    bridge = sum(row[2] for row in summary_rows)
    total = native + bridge
    if language == "en":
        title = "# Command reference"
        intro = f"{native} **UAIP commands** and {bridge} **Toolset bridge commands**, a combined total of {total}."
        summary_heading = "## Domain summary"
        summary_header = "| Group | Provider | UAIP commands | Toolset bridge | Demo |"
        selector_heading = "## Choosing which play world a Runtime command acts on"
        selector_sentence = f"{len(selector_entries)} Runtime commands therefore take the selector."
        selector_header = "| Domain | Commands |"
    else:
        title = "# コマンドリファレンス"
        intro = (
            f"{native} 個の **UAIP コマンド** と {bridge} 個の **Toolset ブリッジコマンド** があり、"
            f"合計 {total} です。"
        )
        summary_heading = "## ドメインサマリ"
        summary_header = "| グループ | プロバイダー | UAIP コマンド | Toolset ブリッジ | デモ |"
        selector_heading = "## 実行時コマンドの対象プレイワールドを指定する"
        selector_sentence = f"そのため {len(selector_entries)} 個の実行時コマンドが対象を指定できます。"
        selector_header = "| ドメイン | コマンド |"
    lines = [title, "", intro, "", summary_heading, "", summary_header, "|---|---|---|---|---|"]
    for prefix, native_count, bridge_count, demo in summary_rows:
        lines.append(f"| Editor | `{prefix}` | {native_count} | {bridge_count} | {demo} |")
    lines.extend(["", body.strip("\n"), "", selector_heading, "", selector_sentence, ""])
    lines.extend([selector_header, "|---|---|"])
    lines.extend(f"| `{domain}` | `{name}` |" for domain, name in selector_entries)
    lines.append("")
    return "\n".join(lines)


def base_body(language: str) -> str:
    """Return the domain sections of the baseline document."""
    return "\n".join([
        f"## {ALPHA}",
        "",
        heading(language, "section_a", 2),
        "",
        table_markdown(language, ["🆓 `Foo`", "`Bar`"]),
        "",
        heading(language, "section_b", 1),
        "",
        table_markdown(language, ["`Baz`"]),
        "",
        heading(language, "bridges", 2),
        "",
        table_markdown(language, ["`Toolset.Editor.Alpha.One`", "`Toolset.Editor.Alpha.Two`"]),
        "",
        f"## {BETA}",
        "",
        heading(language, "main", 2),
        "",
        table_markdown(language, ["`Qux`", "`Quux`"]),
        "",
        heading(language, "subset", 2, level=4),
        "",
        "Prose that points at Qux and Quux.",
        "",
        heading(language, "prose", 4),
        "",
        "Prose only.",
    ])


def base_documents() -> tuple[str, str]:
    """Return the (English, Japanese) baseline pair. It is consistent."""
    selector = [(ALPHA, "Foo")]
    return (
        render_document("en", BASE_SUMMARY, base_body("en"), selector),
        render_document("ja", BASE_SUMMARY, base_body("ja"), selector),
    )


def base_exceptions() -> dict[str, object]:
    """Return the exception file that goes with the baseline pair."""
    return {
        "schema_version": 1,
        "max_entries": 10,
        "exceptions": [
            {
                "kind": "prose-only-bridge",
                "domain": BETA,
                "heading": {"en": "Toolset bridges", "ja": "Toolset ブリッジ"},
                "toolset_providers": ["Toolset.Editor.Beta"],
                "reason": "Described in prose.",
            },
            {
                "kind": "subset-heading",
                "domain": BETA,
                "heading": {"en": "Subset note", "ja": "サブセット注記"},
                "members": ["Qux", "Quux"],
                "reason": "Points at two rows of the table above.",
            },
        ],
    }


def replace_once(text: str, old: str, new: str) -> str:
    """Replace the only occurrence of `old`; fail loudly when the fixture changed under the test."""
    occurrences = text.count(old)
    if occurrences != 1:
        raise AssertionError(f"expected exactly one occurrence of {old!r} in the fixture, found {occurrences}")
    return text.replace(old, new)


def edited(pair: tuple[str, str], language: str, old: str, new: str) -> tuple[str, str]:
    """Edit the English document, the Japanese one or both ("both")."""
    english, japanese = pair
    if language in ("en", "both"):
        english = replace_once(english, old, new)
    if language in ("ja", "both"):
        japanese = replace_once(japanese, old, new)
    return english, japanese


def edit_heading(
    pair: tuple[str, str],
    key: str,
    old_number: int | None,
    new_number: int | None,
    language: str = "both",
    level: int = 3,
) -> tuple[str, str]:
    """Change the count of a baseline heading (None removes the count)."""
    result = pair
    for code in ("en", "ja"):
        if language in (code, "both"):
            old = heading(code, key, old_number, level)
            new = heading(code, key, new_number, level)
            result = edited(result, code, old, new)
    return result


def insert_before_beta(pair: tuple[str, str], language: str, new_text: str) -> tuple[str, str]:
    """Insert Markdown at the end of the ALPHA section."""
    return edited(pair, language, f"## {BETA}", new_text + f"\n## {BETA}")


def run_check(
    english: str,
    japanese: str,
    exceptions: dict[str, object] | str | None = None,
) -> tuple[counts.Evaluation, dict[str, object]]:
    """Run the checks on two texts. Raises NoVerdictError when no verdict is possible."""
    if exceptions is None:
        exceptions_text = json.dumps(base_exceptions())
    elif isinstance(exceptions, str):
        exceptions_text = exceptions
    else:
        exceptions_text = json.dumps(exceptions)
    return counts.check_texts(english, japanese, exceptions_text, {"mode": "files"})


def check_ids(evaluation: counts.Evaluation) -> set[str]:
    """Return the set of check ids that have a finding."""
    return {finding.check for finding in evaluation.findings}


def findings_of(evaluation: counts.Evaluation, check: str, language: str | None = None) -> list[counts.Finding]:
    """Return the findings of one check, optionally of one language."""
    return [
        finding
        for finding in evaluation.findings
        if finding.check == check and (language is None or finding.language == language)
    ]


def messages_of(evaluation: counts.Evaluation, check: str, language: str | None = None) -> list[str]:
    """Return the messages of the findings of one check, optionally of one language."""
    return [finding.message for finding in findings_of(evaluation, check, language)]


def line_of(text: str, needle: str) -> int:
    """Return the 1-based number of the first line that equals `needle`."""
    for index, line in enumerate(text.split("\n")):
        if line == needle:
            return index + 1
    raise AssertionError(f"no line equals {needle!r}")


def exceptions_with(mutator: Callable[[dict[str, object]], None]) -> dict[str, object]:
    """Return a copy of the baseline exception file edited by `mutator`."""
    data = base_exceptions()
    mutator(data)
    return copy.deepcopy(data)


def no_exceptions() -> dict[str, object]:
    """Return an exception file with no entries."""
    return {"schema_version": 1, "max_entries": 10, "exceptions": []}


def entries_of(data: dict[str, object]) -> list[dict[str, object]]:
    """Return the entry list of an exception file dictionary."""
    entries = data["exceptions"]
    assert isinstance(entries, list)
    return entries


def run_main(
    english: str | bytes,
    japanese: str | bytes,
    exceptions_text: str | bytes,
    extra_arguments: Sequence[str] = (),
) -> tuple[int, str, str]:
    """Run main() on files in a temporary directory. Returns (exit code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as directory:
        paths: dict[str, Path] = {}
        for name, value in (("en.md", english), ("ja.md", japanese), ("exceptions.json", exceptions_text)):
            payload = (value if isinstance(value, bytes) else value.encode("utf-8"))
            paths[name] = Path(directory) / name
            paths[name].write_bytes(payload)
        arguments = [
            "--en",
            str(paths["en.md"]),
            "--ja",
            str(paths["ja.md"]),
            "--exceptions",
            str(paths["exceptions.json"]),
            *extra_arguments,
        ]
        standard_output = io.StringIO()
        standard_error = io.StringIO()
        with contextlib.redirect_stdout(standard_output), contextlib.redirect_stderr(standard_error):
            exit_code = counts.main(arguments)
    return exit_code, standard_output.getvalue(), standard_error.getvalue()


# --------------------------------------------------------------------------------------
# Baseline
# --------------------------------------------------------------------------------------


class BaselineTest(unittest.TestCase):
    """The unmodified pair is consistent and every check looks at something."""

    def test_baseline_is_consistent(self) -> None:
        """The baseline pair has no finding."""
        evaluation, report = run_check(*base_documents())
        self.assertEqual(evaluation.findings, ())
        self.assertEqual(report["verdict"], "consistent")

    def test_every_check_looks_at_items(self) -> None:
        """A check that saw nothing could not have failed; the baseline gives each of them input."""
        evaluation, _ = run_check(*base_documents())
        for check in ALL_CHECKS:
            with self.subTest(check=check):
                self.assertGreater(evaluation.reach.get(check, 0), 0)

    def test_bridge_names_carry_no_domain_prefix(self) -> None:
        """A bridge row keeps its full name; a native row gets the section prefix."""
        _, report = run_check(*base_documents())
        bridge = report["bridge"]
        assert isinstance(bridge, dict)
        expected_bridge = ["Toolset.Editor.Alpha.One", "Toolset.Editor.Alpha.Two"]
        expected_native = sorted([
            "UAIP.Editor.Alpha.Foo",
            "UAIP.Editor.Alpha.Bar",
            "UAIP.Editor.Alpha.Baz",
            "UAIP.Editor.Beta.Qux",
            "UAIP.Editor.Beta.Quux",
        ])
        self.assertEqual(bridge["listed_names"], {"en": expected_bridge, "ja": expected_bridge})
        self.assertEqual(report["native_names"], {"en": expected_native, "ja": expected_native})

    def test_toolset_summary_row_takes_the_bridge_rows_with_its_prefix(self) -> None:
        """A summary row with a `Toolset.` prefix owns the bridge rows that start with it."""
        pair = edited(base_documents(), "both", ALPHA_SUMMARY_ROW, ALPHA_SUMMARY_ROW.replace("| 2 |", "| 1 |"))
        pair = edited(
            pair,
            "both",
            "| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |",
            "| Editor | `Toolset.Editor.Gamma` | — | 1 | — |\n| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |",
        )
        pair = edited(pair, "both", "`Toolset.Editor.Alpha.Two`", "`Toolset.Editor.Gamma.One`")
        evaluation, _ = run_check(*pair)
        self.assertEqual(evaluation.findings, ())

    def test_toolset_summary_row_without_matching_rows_is_a_k2(self) -> None:
        """The same summary row without a bridge row under its prefix does not balance."""
        pair = edited(base_documents(), "both", ALPHA_SUMMARY_ROW, ALPHA_SUMMARY_ROW.replace("| 2 |", "| 1 |"))
        pair = edited(
            pair,
            "both",
            "| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |",
            "| Editor | `Toolset.Editor.Gamma` | — | 1 | — |\n| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |",
        )
        evaluation, _ = run_check(*pair)
        gamma = [finding for finding in findings_of(evaluation, "K2") if finding.domain == "Toolset.Editor.Gamma"]
        self.assertEqual(len(gamma), 2)


# --------------------------------------------------------------------------------------
# K1 to K8
# --------------------------------------------------------------------------------------


class TotalsCheckTest(unittest.TestCase):
    """K1: the opening totals, the summary totals and the listed commands agree."""

    def test_opening_native_total_off_by_one(self) -> None:
        """An opening paragraph that says 6 where the table adds up to 5."""
        pair = edited(base_documents(), "en", "5 **UAIP commands**", "6 **UAIP commands**")
        evaluation, _ = run_check(*pair)
        found = findings_of(evaluation, "K1", "en")
        self.assertIn((5, 6), [(finding.expected, finding.actual) for finding in found])
        self.assertEqual(findings_of(evaluation, "K1", "ja"), [])

    def test_opening_total_that_is_not_native_plus_bridge(self) -> None:
        """A combined total of 12 in both languages is wrong against 5 + 6 and against the table."""
        pair = edited(base_documents(), "en", "combined total of 11", "combined total of 12")
        pair = edited(pair, "ja", "合計 11", "合計 12")
        evaluation, _ = run_check(*pair)
        self.assertEqual(check_ids(evaluation), {"K1"})
        self.assertEqual({finding.language for finding in findings_of(evaluation, "K1")}, {"en", "ja"})

    def test_summary_total_differs_from_the_listed_commands(self) -> None:
        """A summary table that adds up to more than the commands that are listed."""
        pair = edited(base_documents(), "both", "| 2 | 4 | — |", "| 2 | 5 | — |")
        evaluation, _ = run_check(*pair)
        found = [finding for finding in findings_of(evaluation, "K1", "en") if finding.expected == 6]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].actual, 7)

    def test_prose_only_count_flows_into_the_bridge_total(self) -> None:
        """Raising the prose-only count without the totals breaks K1 and K2."""
        pair = edit_heading(base_documents(), "prose", 4, 5)
        evaluation, _ = run_check(*pair)
        self.assertTrue({"K1", "K2"} <= check_ids(evaluation))


class SummaryRowCheckTest(unittest.TestCase):
    """K2: each summary row agrees with its domain section, in both directions."""

    def test_summary_row_overstates_the_section(self) -> None:
        """The summary row says 4 where the section lists 3."""
        pair = edited(base_documents(), "both", ALPHA_SUMMARY_ROW, ALPHA_SUMMARY_ROW.replace("| 3 |", "| 4 |"))
        evaluation, _ = run_check(*pair)
        found = [finding for finding in findings_of(evaluation, "K2", "en") if finding.domain == ALPHA]
        self.assertEqual([(finding.expected, finding.actual) for finding in found], [(4, 3)])

    def test_section_with_commands_but_no_summary_row(self) -> None:
        """A domain section that lists commands must have a summary row."""
        pair = edited(base_documents(), "both", "| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |\n", "")
        evaluation, _ = run_check(*pair)
        missing = [finding for finding in findings_of(evaluation, "K2", "en") if finding.domain == BETA]
        self.assertTrue(any("no row in the summary" in finding.message for finding in missing))

    def test_summary_row_prefix_listed_twice(self) -> None:
        """The same prefix twice in the summary table is reported."""
        row = "| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |"
        pair = edited(base_documents(), "en", row, row + "\n" + row)
        evaluation, _ = run_check(*pair)
        self.assertTrue(any("more than once" in finding.message for finding in findings_of(evaluation, "K2", "en")))


class HeadingCountCheckTest(unittest.TestCase):
    """K3: the (N) of a sub-heading equals the command rows in its range."""

    def test_heading_count_off_by_one(self) -> None:
        """Section A says 3 and lists 2: one K3 on the English heading line."""
        pair = edit_heading(base_documents(), "section_a", 2, 3, language="en")
        evaluation, _ = run_check(*pair)
        found = findings_of(evaluation, "K3")
        self.assertEqual(len(found), 1)
        self.assertEqual((found[0].language, found[0].expected, found[0].actual), ("en", 3, 2))
        self.assertEqual(found[0].line, line_of(pair[0], heading("en", "section_a", 3)))

    def test_heading_count_that_agrees_is_quiet(self) -> None:
        """The baseline has four counted headings and no K3."""
        evaluation, _ = run_check(*base_documents())
        self.assertEqual(findings_of(evaluation, "K3"), [])

    def test_wrong_count_on_a_prose_only_heading_is_not_a_k3(self) -> None:
        """The heading handled by an exception is not compared with its (empty) range."""
        pair = edit_heading(base_documents(), "prose", 4, 9)
        evaluation, _ = run_check(*pair)
        self.assertEqual(findings_of(evaluation, "K3"), [])

    def test_rich_count_notation_in_a_heading(self) -> None:
        """`(N, ...)` in English and `（N、...）` in Japanese are read as counts."""
        pair = edited(base_documents(), "en", heading("en", "section_a", 2), "### Section A (2, Foo and Bar)")
        pair = edited(pair, "ja", heading("ja", "section_a", 2), "### セクション A（2、Foo と Bar）")
        evaluation, _ = run_check(*pair)
        self.assertEqual(evaluation.findings, ())

    def test_rich_count_notation_with_a_wrong_number(self) -> None:
        """The number in the rich notation is compared like any other."""
        pair = edited(base_documents(), "en", heading("en", "section_a", 2), "### Section A (3, Foo and Bar)")
        pair = edited(pair, "ja", heading("ja", "section_a", 2), "### セクション A（3、Foo と Bar）")
        evaluation, _ = run_check(*pair)
        self.assertEqual({finding.language for finding in findings_of(evaluation, "K3")}, {"en", "ja"})

    def test_japanese_counts_with_a_unit_word(self) -> None:
        """`（N 件）` and `（N コマンド）` are read as counts."""
        for suffix in ("2 件", "2 コマンド", "2件"):
            with self.subTest(suffix=suffix):
                pair = edited(
                    base_documents(),
                    "ja",
                    heading("ja", "section_a", 2),
                    f"### セクション A（{suffix}）",
                )
                evaluation, _ = run_check(*pair)
                self.assertEqual(evaluation.findings, ())

    def test_parse_count_heading_notations(self) -> None:
        """The notations of both languages, a decorated title and a count inside backticks."""
        english = counts.ENGLISH_PROFILE
        japanese = counts.JAPANESE_PROFILE
        self.assertEqual(counts.parse_count_heading("Section A (2)", english), (2, "Section A"))
        self.assertEqual(counts.parse_count_heading("Section A (2, Foo)", english), (2, "Section A"))
        self.assertEqual(counts.parse_count_heading("Free 🆓 (3)", english), (3, "Free"))
        self.assertEqual(counts.parse_count_heading("セクション（2、Foo）", japanese), (2, "セクション"))
        self.assertEqual(counts.parse_count_heading("セクション（4 件）", japanese), (4, "セクション"))
        self.assertIsNone(counts.parse_count_heading("No count here", english))
        self.assertIsNone(counts.parse_count_heading("Use `Foo(2)` here", english))

    def test_notation_of_the_other_language_is_not_a_count(self) -> None:
        """A full-width count in an English heading must not vanish from the checks silently."""
        pair = edited(base_documents(), "en", heading("en", "section_a", 2), "### Section A（2）")
        with self.assertRaises(counts.NoVerdictError):
            run_check(*pair)
        pair = edited(base_documents(), "ja", heading("ja", "section_a", 2), "### セクション A (2)")
        with self.assertRaises(counts.NoVerdictError):
            run_check(*pair)


class HeadingTableCheckTest(unittest.TestCase):
    """K4: a counted sub-heading needs a command table with rows."""

    def test_counted_heading_without_a_table(self) -> None:
        """K4 on both languages, and the heading is not reported a second time as K3."""
        pair = insert_before_beta(base_documents(), "en", "### Empty section (1)\n\nNothing here.\n")
        pair = insert_before_beta(pair, "ja", "### 空の節（1）\n\nここには何もない。\n")
        evaluation, _ = run_check(*pair)
        self.assertEqual(check_ids(evaluation), {"K4"})
        self.assertEqual({finding.language for finding in findings_of(evaluation, "K4")}, {"en", "ja"})

    def test_counted_heading_with_an_empty_table(self) -> None:
        """A table with a header and no rows is also K4, with its own wording."""
        empty = table_markdown("en", [])
        pair = insert_before_beta(base_documents(), "en", f"### Empty section (1)\n\n{empty}\n")
        pair = insert_before_beta(pair, "ja", f"### 空の節（1）\n\n{table_markdown('ja', [])}\n")
        evaluation, _ = run_check(*pair)
        self.assertEqual(check_ids(evaluation), {"K4"})
        self.assertTrue(all("no command rows" in finding.message for finding in findings_of(evaluation, "K4")))

    def test_heading_with_rows_is_not_a_k4(self) -> None:
        """The baseline's counted headings all have rows."""
        evaluation, _ = run_check(*base_documents())
        self.assertEqual(findings_of(evaluation, "K4"), [])


class LanguageAgreementCheckTest(unittest.TestCase):
    """K5: the English and the Japanese document state the same values."""

    def test_opening_total_differs(self) -> None:
        """The English opening paragraph differs from the Japanese one."""
        pair = edited(base_documents(), "en", "5 **UAIP commands**", "6 **UAIP commands**")
        evaluation, _ = run_check(*pair)
        self.assertTrue(any("opening native total" in finding.message for finding in findings_of(evaluation, "K5")))

    def test_summary_value_differs(self) -> None:
        """One language's summary row has another bridge count."""
        pair = edited(base_documents(), "ja", ALPHA_SUMMARY_ROW, ALPHA_SUMMARY_ROW.replace("| 2 |", "| 3 |"))
        evaluation, _ = run_check(*pair)
        self.assertTrue(any("bridge: en 2, ja 3" in finding.message for finding in findings_of(evaluation, "K5")))

    def test_summary_row_present_in_one_language_only(self) -> None:
        """A summary row that only one language has."""
        pair = edited(base_documents(), "ja", "| Editor | `UAIP.Editor.Beta` | 2 | 4 | — |\n", "")
        evaluation, _ = run_check(*pair)
        self.assertTrue(any("exists only in en" in finding.message for finding in findings_of(evaluation, "K5")))

    def test_command_names_differ(self) -> None:
        """A command that is named differently in the two documents."""
        pair = edited(base_documents(), "ja", "| 🆓 `Foo` | desc |", "| 🆓 `Fooo` | desc |")
        evaluation, _ = run_check(*pair)
        names = [finding for finding in findings_of(evaluation, "K5") if "commands differ" in finding.message]
        self.assertTrue(any(finding.domain == ALPHA for finding in names))

    def test_demo_marks_differ(self) -> None:
        """The same command is free in one language and not in the other."""
        pair = edited(base_documents(), "ja", "| 🆓 `Foo` | desc |", "| `Foo` | desc |")
        evaluation, _ = run_check(*pair)
        self.assertIn("demo-marked commands differ", " ".join(messages_of(evaluation, "K5")))

    def test_selector_count_differs(self) -> None:
        """The two selector sentences state different numbers."""
        pair = edited(base_documents(), "ja", "そのため 1 個の", "そのため 2 個の")
        evaluation, _ = run_check(*pair)
        self.assertTrue(any("selector count" in finding.message for finding in findings_of(evaluation, "K5")))

    def test_selector_names_differ(self) -> None:
        """The two selector tables list different commands."""
        pair = edited(base_documents(), "ja", "| `UAIP.Editor.Alpha` | `Foo` |", "| `UAIP.Editor.Alpha` | `Bar` |")
        evaluation, _ = run_check(*pair)
        self.assertIn("selector table names differ", " ".join(messages_of(evaluation, "K5")))

    def test_innermost_heading_count_differs_per_command(self) -> None:
        """A command that sits under a counted heading in one language and an uncounted one in the other."""
        pair = edit_heading(base_documents(), "section_a", 2, None, language="ja")
        evaluation, _ = run_check(*pair)
        found = [finding for finding in findings_of(evaluation, "K5") if "sits under a heading" in finding.message]
        self.assertEqual(len(found), 2)
        self.assertEqual({(finding.expected, finding.actual) for finding in found}, {(2, None)})


class SelectorCheckTest(unittest.TestCase):
    """K6: the selector sentence agrees with the table and the table with the sections."""

    def test_sentence_states_the_wrong_number(self) -> None:
        """The sentence says 2 and the table lists 1."""
        pair = edited(base_documents(), "en", "1 Runtime commands therefore", "2 Runtime commands therefore")
        evaluation, _ = run_check(*pair)
        found = findings_of(evaluation, "K6", "en")
        self.assertEqual([(finding.expected, finding.actual) for finding in found], [(2, 1)])

    def test_listed_name_is_not_a_row_of_the_domain(self) -> None:
        """The table lists a command that the domain section does not have."""
        pair = edited(base_documents(), "en", "| `UAIP.Editor.Alpha` | `Foo` |", "| `UAIP.Editor.Alpha` | `Nothing` |")
        evaluation, _ = run_check(*pair)
        self.assertIn("no such command row", " ".join(messages_of(evaluation, "K6", "en")))

    def test_name_listed_twice(self) -> None:
        """A duplicated name is a finding of its own, on top of the count."""
        row = "| `UAIP.Editor.Alpha` | `Foo` |"
        pair = edited(base_documents(), "en", row, row + "\n" + row)
        evaluation, _ = run_check(*pair)
        self.assertTrue(any("twice" in finding.message for finding in findings_of(evaluation, "K6", "en")))


class DemoColumnCheckTest(unittest.TestCase):
    """K7: the Demo column agrees with the demo marks of the command rows."""

    def test_all_free_summary_with_a_partial_section(self) -> None:
        """`✅` where only one of three is marked."""
        pair = edited(base_documents(), "both", "| 3 | 2 | partial (1/3) |", "| 3 | 2 | ✅ |")
        evaluation, _ = run_check(*pair)
        found = findings_of(evaluation, "K7", "en")
        self.assertEqual([(finding.domain, finding.expected, finding.actual) for finding in found],
                         [(ALPHA, "partial (1/3)", "✅")])

    def test_none_summary_with_a_marked_row(self) -> None:
        """`—` where a row is marked."""
        pair = edited(base_documents(), "both", "| 3 | 2 | partial (1/3) |", "| 3 | 2 | — |")
        evaluation, _ = run_check(*pair)
        self.assertEqual(check_ids(evaluation), {"K7"})

    def test_partial_summary_with_the_wrong_numbers(self) -> None:
        """`partial (2/3)` where one is marked."""
        pair = edited(base_documents(), "both", "| 3 | 2 | partial (1/3) |", "| 3 | 2 | partial (2/3) |")
        evaluation, _ = run_check(*pair)
        self.assertEqual(check_ids(evaluation), {"K7"})

    def test_all_free_summary_with_every_row_marked_is_quiet(self) -> None:
        """The positive side of `✅`."""
        pair = edited(base_documents(), "both", "| `Bar` | desc |", "| 🆓 `Bar` | desc |")
        pair = edited(pair, "both", "| `Baz` | desc |", "| 🆓 `Baz` | desc |")
        pair = edited(pair, "both", "| 3 | 2 | partial (1/3) |", "| 3 | 2 | ✅ |")
        evaluation, _ = run_check(*pair)
        self.assertEqual(evaluation.findings, ())

    def test_demo_mark_on_a_bridge_row_is_not_counted(self) -> None:
        """Only UAIP rows count for the Demo column."""
        old_row = "| `Toolset.Editor.Alpha.One` | desc |"
        pair = edited(base_documents(), "both", old_row, old_row.replace("| `", "| 🆓 `"))
        evaluation, _ = run_check(*pair)
        self.assertEqual(evaluation.findings, ())

    def test_sentence_at_the_start_of_a_line_covers_the_next_table(self) -> None:
        """A table that follows "Not provided in the demo build." must have no demo mark."""
        phrases = {
            "en": ("Not provided in the demo build.",),
            "ja": ("デモ版には含まれません。", "デモ版では提供されません。"),
        }
        for language, sentences in phrases.items():
            for sentence in sentences:
                with self.subTest(language=language, sentence=sentence):
                    pair = base_documents()
                    for code in ("en", "ja"):
                        section = heading(code, "section_b", 1)
                        phrase = (sentence if code == language else phrases[code][0])
                        pair = edited(pair, code, section + "\n", f"{section}\n\n{phrase}\n")
                    pair = edited(pair, "both", "| `Baz` | desc |", "| 🆓 `Baz` | desc |")
                    pair = edited(pair, "both", "| 3 | 2 | partial (1/3) |", "| 3 | 2 | partial (2/3) |")
                    evaluation, _ = run_check(*pair)
                    self.assertEqual(check_ids(evaluation), {"K7"})
                    conflicts = [finding for finding in findings_of(evaluation, "K7", language)]
                    self.assertEqual(len(conflicts), 1)
                    language_text = pair[("en", "ja").index(language)]
                    self.assertEqual(conflicts[0].line, line_of(language_text, "| 🆓 `Baz` | desc |"))

    def test_sentence_inside_a_paragraph_does_not_cover_the_next_table(self) -> None:
        """A sentence that is about one named command is not about the table that follows it."""
        sentences = {
            "en": "The command `Baz` is flagged: Not provided in the demo build.",
            "ja": "コマンド `Baz` は デモ版には含まれません。",
        }
        pair = base_documents()
        for code in ("en", "ja"):
            section = heading(code, "section_b", 1)
            pair = edited(pair, code, section + "\n", f"{section}\n\n{sentences[code]}\n")
        pair = edited(pair, "both", "| `Baz` | desc |", "| 🆓 `Baz` | desc |")
        pair = edited(pair, "both", "| 3 | 2 | partial (1/3) |", "| 3 | 2 | partial (2/3) |")
        evaluation, _ = run_check(*pair)
        self.assertEqual(evaluation.findings, ())

    def test_parser_records_only_a_sentence_that_opens_its_line(self) -> None:
        """The parsed document shows the same distinction without running the checks."""
        pair = base_documents()
        section = heading("en", "section_b", 1)
        marked = edited(pair, "en", "| `Baz` | desc |", "| 🆓 `Baz` | desc |")[0]
        opening = marked.replace(section + "\n", f"{section}\n\nNot provided in the demo build.\n")
        inline = marked.replace(section + "\n", f"{section}\n\nMore: Not provided in the demo build.\n")
        self.assertEqual(len(counts.parse_document(opening, "en").demo_conflicts), 1)
        self.assertEqual(len(counts.parse_document(inline, "en").demo_conflicts), 0)


class DuplicateNameCheckTest(unittest.TestCase):
    """K8: a fully-qualified name is listed once per language."""

    def test_duplicate_row_with_every_total_raised_is_still_found(self) -> None:
        """Adding a duplicate row and raising the heading, the summary and the totals leaves only K8."""
        pair = edited(base_documents(), "both", "| `Bar` | desc |", "| `Bar` | desc |\n| `Bar` | desc |")
        pair = edit_heading(pair, "section_a", 2, 3)
        pair = edited(pair, "both", ALPHA_SUMMARY_ROW, "| Editor | `UAIP.Editor.Alpha` | 4 | 2 | partial (1/4) |")
        pair = edited(pair, "en", "5 **UAIP commands**", "6 **UAIP commands**")
        pair = edited(pair, "en", "combined total of 11", "combined total of 12")
        pair = edited(pair, "ja", "5 個の **UAIP コマンド**", "6 個の **UAIP コマンド**")
        pair = edited(pair, "ja", "合計 11", "合計 12")
        evaluation, _ = run_check(*pair)
        self.assertEqual(check_ids(evaluation), {"K8"})
        found = findings_of(evaluation, "K8")
        self.assertEqual({finding.language for finding in found}, {"en", "ja"})
        self.assertTrue(all((finding.expected, finding.actual) == (1, 2) for finding in found))

    def test_unique_names_are_quiet(self) -> None:
        """The baseline lists every name once."""
        evaluation, _ = run_check(*base_documents())
        self.assertEqual(findings_of(evaluation, "K8"), [])


# --------------------------------------------------------------------------------------
# Exception file
# --------------------------------------------------------------------------------------


class ExceptionRuleTest(unittest.TestCase):
    """The rules for the exception file."""

    def test_entry_without_a_matching_heading_is_stale(self) -> None:
        """Zero matches: the entry is reported as stale for that language only."""
        pair = edited(base_documents(), "ja", heading("ja", "prose", 4), "### 別名（4）")
        evaluation, _ = run_check(*pair)
        stale = findings_of(evaluation, "EXC")
        self.assertEqual([(finding.language, finding.line) for finding in stale], [("ja", 0)])
        self.assertIn("stale", stale[0].message)

    def test_prose_only_entry_whose_heading_gets_rows_is_stale(self) -> None:
        """A prose-only heading that now lists a command row no longer needs its entry."""
        row_table = table_markdown("en", ["`Toolset.Editor.Beta.X`"])
        pair = edited(base_documents(), "en", "Prose only.", f"Prose only.\n\n{row_table}")
        evaluation, _ = run_check(*pair)
        stale = findings_of(evaluation, "EXC", "en")
        self.assertEqual(len(stale), 1)
        self.assertIn("prose-only-bridge", stale[0].message)

    def test_subset_entry_whose_heading_gets_a_table_is_stale(self) -> None:
        """A subset heading with its own command table no longer needs its entry."""
        row_table = table_markdown("en", ["`Zed`"])
        pair = edited(base_documents(), "en", "Prose that points at Qux and Quux.", f"{row_table}")
        evaluation, _ = run_check(*pair)
        stale = findings_of(evaluation, "EXC", "en")
        self.assertEqual(len(stale), 1)
        self.assertIn("subset-heading", stale[0].message)

    def test_entry_matching_two_headings_is_no_verdict(self) -> None:
        """More than one match is ambiguous, not stale."""
        extra = heading("en", "subset", 1, level=4) + "\n\nMore prose.\n"
        pair = edited(base_documents(), "en", heading("en", "prose", 4), extra + "\n" + heading("en", "prose", 4))
        with self.assertRaises(counts.NoVerdictError):
            run_check(*pair)

    def test_entry_limit(self) -> None:
        """More entries than `max_entries` is a finding; exactly as many is not."""
        too_many = exceptions_with(lambda data: data.update(max_entries=1))
        evaluation, _ = run_check(*base_documents(), too_many)
        found = findings_of(evaluation, "EXC")
        self.assertEqual([(finding.language, finding.line, finding.expected, finding.actual) for finding in found],
                         [("en", 0, 1, 2)])
        exact = exceptions_with(lambda data: data.update(max_entries=2))
        evaluation, _ = run_check(*base_documents(), exact)
        self.assertEqual(evaluation.findings, ())

    def test_subset_members_must_match_the_count_and_the_rows(self) -> None:
        """A member list of the wrong length, or naming a row that does not exist, is a K3."""
        short = exceptions_with(lambda data: entries_of(data)[1].update(members=["Qux"]))
        evaluation, _ = run_check(*base_documents(), short)
        self.assertEqual({finding.language for finding in findings_of(evaluation, "K3")}, {"en", "ja"})
        unknown = exceptions_with(lambda data: entries_of(data)[1].update(members=["Qux", "Nope"]))
        evaluation, _ = run_check(*base_documents(), unknown)
        self.assertTrue(any("not a command row" in finding.message for finding in findings_of(evaluation, "K3")))

    def test_malformed_exception_files_are_no_verdict(self) -> None:
        """Unknown kinds and keys, wrong types and a missing language all end the run."""
        def set_kind(data: dict[str, object]) -> None:
            entries_of(data)[0]["kind"] = "other"

        def add_unknown_key(data: dict[str, object]) -> None:
            entries_of(data)[0]["extra"] = 1

        def add_unknown_top_key(data: dict[str, object]) -> None:
            data["extra"] = 1

        def drop_reason(data: dict[str, object]) -> None:
            del entries_of(data)[0]["reason"]

        def members_as_string(data: dict[str, object]) -> None:
            entries_of(data)[1]["members"] = "Qux"

        def empty_providers(data: dict[str, object]) -> None:
            entries_of(data)[0]["toolset_providers"] = []

        def provider_without_prefix(data: dict[str, object]) -> None:
            entries_of(data)[0]["toolset_providers"] = ["Editor.Beta"]

        def limit_as_string(data: dict[str, object]) -> None:
            data["max_entries"] = "10"

        def limit_as_bool(data: dict[str, object]) -> None:
            data["max_entries"] = True

        def limit_negative(data: dict[str, object]) -> None:
            data["max_entries"] = -1

        def schema_version_two(data: dict[str, object]) -> None:
            data["schema_version"] = 2

        def entries_as_object(data: dict[str, object]) -> None:
            data["exceptions"] = {}

        def entry_as_string(data: dict[str, object]) -> None:
            entries_of(data)[0] = "text"

        def heading_without_japanese(data: dict[str, object]) -> None:
            entries_of(data)[0]["heading"] = {"en": "Toolset bridges"}

        def heading_with_extra_language(data: dict[str, object]) -> None:
            entries_of(data)[0]["heading"] = {"en": "a", "ja": "b", "fr": "c"}

        def empty_domain(data: dict[str, object]) -> None:
            entries_of(data)[0]["domain"] = ""

        def provider_in_two_entries(data: dict[str, object]) -> None:
            duplicate = copy.deepcopy(entries_of(data)[0])
            duplicate["heading"] = {"en": "Other", "ja": "別"}
            entries_of(data).append(duplicate)

        def provider_twice_in_one_entry(data: dict[str, object]) -> None:
            entries_of(data)[0]["toolset_providers"] = ["Toolset.Editor.Beta", "Toolset.Editor.Beta"]

        def repeated_heading_key(data: dict[str, object]) -> None:
            duplicate = copy.deepcopy(entries_of(data)[1])
            entries_of(data).append(duplicate)

        mutators = [
            set_kind, add_unknown_key, add_unknown_top_key, drop_reason, members_as_string, empty_providers,
            provider_without_prefix, limit_as_string, limit_as_bool, limit_negative, schema_version_two,
            entries_as_object, entry_as_string, heading_without_japanese, heading_with_extra_language, empty_domain,
            provider_in_two_entries, provider_twice_in_one_entry, repeated_heading_key,
        ]
        for mutator in mutators:
            with self.subTest(mutator=mutator.__name__):
                with self.assertRaises(counts.NoVerdictError):
                    run_check(*base_documents(), exceptions_with(mutator))

    def test_exception_file_that_is_not_json_is_no_verdict(self) -> None:
        """Text that is not JSON, or JSON that is not an object."""
        for text in ("{", "[]", ""):
            with self.subTest(text=text):
                with self.assertRaises(counts.NoVerdictError):
                    run_check(*base_documents(), text)

    def test_real_exception_file_is_valid_and_within_its_limit(self) -> None:
        """The shipped exception file parses and its limit is the reviewed number."""
        text = (SCRIPT_DIRECTORY / counts.EXCEPTIONS_PATH.rsplit("/", 1)[1]).read_text(encoding="utf-8")
        exception_set = counts.parse_exceptions(text)
        self.assertEqual(exception_set.max_entries, EXPECTED_MAX_ENTRIES)
        self.assertLessEqual(len(exception_set.entries), exception_set.max_entries)


# --------------------------------------------------------------------------------------
# Unreadable input
# --------------------------------------------------------------------------------------


class UnreadableInputTest(unittest.TestCase):
    """A structure the checks cannot read ends the run with exit 2 instead of passing."""

    def test_unreadable_documents(self) -> None:
        """Each of these inputs has no verdict."""
        cases = {
            "non-count number in a heading": edited(base_documents(), "en", "### Section A (2)", "### Section A (v2)"),
            "two counts in a heading": edited(base_documents(), "en", "### Section A (2)", "### Section A (2) (3)"),
            "missing summary heading": edited(base_documents(), "en", "## Domain summary", "## Overview"),
            "summary row with four columns": edited(
                base_documents(), "ja", BETA_SUMMARY_ROW, "| Editor | `UAIP.Editor.Beta` | 2 | 4 |"
            ),
            "summary number that is not a number": edited(
                base_documents(), "en", BETA_SUMMARY_ROW, BETA_SUMMARY_ROW.replace("| 2 |", "| many |")
            ),
            "demo cell that is not understood": edited(
                base_documents(), "en", BETA_SUMMARY_ROW, BETA_SUMMARY_ROW.replace("| — |", "| maybe |")
            ),
            "opening paragraph without the totals": edited(
                base_documents(), "en", ", a combined total of 11", ""
            ),
            "no selector table": edited(base_documents(), "ja", "| ドメイン | コマンド |", "| 別 | 表 |"),
            "empty document": ("", base_documents()[1]),
        }
        for description, pair in cases.items():
            with self.subTest(description=description):
                with self.assertRaises(counts.NoVerdictError):
                    run_check(*pair)

    def test_documents_without_anything_to_check_are_no_verdict(self) -> None:
        """A pair with no domain section, no command row and no counted heading passed nothing."""
        english = render_document("en", [], "")
        japanese = render_document("ja", [], "")
        with self.assertRaises(counts.NoVerdictError):
            run_check(english, japanese)

    def test_exit_code_is_two_for_each_unreadable_input(self) -> None:
        """main() maps all of them to exit 2."""
        english, japanese = base_documents()
        exceptions_text = json.dumps(base_exceptions())
        bad_english = edited((english, japanese), "en", "## Domain summary", "## Overview")[0]
        cases = [
            ("bad heading", bad_english, japanese, exceptions_text),
            ("bad exceptions", english, japanese, "{"),
            ("not UTF-8", b"\xff\xfe\x00bad", japanese, exceptions_text),
        ]
        for description, english_input, japanese_input, exceptions_input in cases:
            with self.subTest(description=description):
                exit_code, standard_output, _ = run_main(english_input, japanese_input, exceptions_input)
                self.assertEqual(exit_code, 2)
                self.assertIn("no verdict", standard_output)

    def test_files_without_exceptions_or_with_one_language_are_exit_two(self) -> None:
        """--en and --ja go together and need --exceptions."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "x.md"
            path.write_text("# x", encoding="utf-8")
            for arguments in (["--en", str(path), "--ja", str(path)], ["--en", str(path)], ["--ja", str(path)]):
                with self.subTest(arguments=arguments):
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(counts.main(arguments), 2)


# --------------------------------------------------------------------------------------
# Line endings and encodings
# --------------------------------------------------------------------------------------


class LineEndingTest(unittest.TestCase):
    """CRLF and a byte-order mark do not change the verdict."""

    def test_crlf_text_gives_the_same_report(self) -> None:
        """The same documents with CRLF line endings give the same report."""
        english, japanese = base_documents()
        _, expected = run_check(english, japanese)
        _, actual = run_check(english.replace("\n", "\r\n"), japanese.replace("\n", "\r\n"))
        self.assertEqual(actual, expected)

    def test_crlf_findings_keep_their_line_numbers(self) -> None:
        """A finding found in CRLF text names the same line as in LF text."""
        pair = edit_heading(base_documents(), "section_a", 2, 3, language="en")
        _, lf_report = run_check(*pair)
        _, crlf_report = run_check(pair[0].replace("\n", "\r\n"), pair[1].replace("\n", "\r\n"))
        self.assertEqual(crlf_report["findings"], lf_report["findings"])
        self.assertNotEqual(lf_report["findings"], [])

    def test_crlf_and_bom_files_are_consistent(self) -> None:
        """main() on CRLF files with a byte-order mark."""
        english, japanese = base_documents()
        exceptions_text = json.dumps(base_exceptions())
        payloads = [("﻿" + text.replace("\n", "\r\n")).encode("utf-8") for text in (english, japanese)]
        exit_code, _, _ = run_main(payloads[0], payloads[1], exceptions_text.replace("\n", "\r\n"))
        self.assertEqual(exit_code, 0)


# --------------------------------------------------------------------------------------
# JSON report
# --------------------------------------------------------------------------------------


class JsonReportTest(unittest.TestCase):
    """The shape of --json and the pairing of exit code and verdict."""

    def run_json(self, english: str | bytes, japanese: str | bytes, exceptions_text: str) -> tuple[int, dict, str]:
        """Run main() with --json and return (exit code, parsed standard output, standard error)."""
        exit_code, standard_output, standard_error = run_main(english, japanese, exceptions_text, ["--json"])
        return exit_code, json.loads(standard_output), standard_error

    def test_consistent_report(self) -> None:
        """Exit 0 and the verdict `consistent`, with the documented keys."""
        exit_code, report, standard_error = self.run_json(*base_documents(), json.dumps(base_exceptions()))
        self.assertEqual(exit_code, 0)
        self.assertEqual(set(report), REPORT_KEYS)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["verdict"], "consistent")
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["source"], {"mode": "files"})
        self.assertEqual(report["selector"], {"en": {"stated": 1, "listed": 1}, "ja": {"stated": 1, "listed": 1}})
        self.assertEqual(report["bridge"]["summary_total"], 6)
        self.assertEqual(
            report["bridge"]["prose_only"],
            [{"domain": BETA, "count": {"en": 4, "ja": 4}, "toolset_providers": ["Toolset.Editor.Beta"]}],
        )
        self.assertEqual(
            report["reach"],
            {"domain_sections": 2, "command_rows": {"en": 7, "ja": 7}, "headings_checked": 12, "exceptions": 2},
        )
        self.assertIn("consistent.", standard_error)

    def test_inconsistent_report(self) -> None:
        """Exit 1 and the verdict `inconsistent`; every finding has the documented keys."""
        pair = edit_heading(base_documents(), "section_a", 2, 3, language="en")
        exit_code, report, _ = self.run_json(*pair, json.dumps(base_exceptions()))
        self.assertEqual(exit_code, 1)
        self.assertEqual(report["verdict"], "inconsistent")
        self.assertGreater(len(report["findings"]), 0)
        for finding in report["findings"]:
            self.assertEqual(set(finding), FINDING_KEYS)
        self.assertEqual(report["findings"][0]["check"], "K3")

    def test_no_verdict_report(self) -> None:
        """Exit 2 and the verdict `no-verdict`; the other keys are still there."""
        pair = edited(base_documents(), "en", "## Domain summary", "## Overview")
        exit_code, report, _ = self.run_json(*pair, json.dumps(base_exceptions()))
        self.assertEqual(exit_code, 2)
        self.assertEqual(set(report), REPORT_KEYS | {"no_verdict_reason"})
        self.assertEqual(report["verdict"], "no-verdict")
        self.assertEqual(report["findings"], [])
        self.assertIsInstance(report["no_verdict_reason"], str)

    def test_standard_output_is_only_json_and_ascii(self) -> None:
        """The report is the whole standard output, and non-ASCII text is escaped."""
        english, japanese = base_documents()
        _, standard_output, standard_error = run_main(english, japanese, json.dumps(base_exceptions()), ["--json"])
        self.assertTrue(standard_output.isascii())
        self.assertTrue(standard_output.lstrip().startswith("{"))
        self.assertIn("K1", standard_error)

    def test_without_json_the_text_goes_to_standard_output(self) -> None:
        """No report is written without --json."""
        english, japanese = base_documents()
        _, standard_output, _ = run_main(english, japanese, json.dumps(base_exceptions()))
        self.assertIn("K1", standard_output)
        self.assertFalse(standard_output.lstrip().startswith("{"))

    def test_input_files_mode_runs_no_git_command(self) -> None:
        """--en --ja does not call git at all."""
        english, japanese = base_documents()
        with mock.patch.object(counts.subprocess, "run", side_effect=AssertionError("git was run")):
            exit_code, _, _ = run_main(english, japanese, json.dumps(base_exceptions()))
        self.assertEqual(exit_code, 0)


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class SourceRevisionTest(unittest.TestCase):
    """`source.rev` is the full commit SHA, whatever name was given."""

    def scrubbed_environment(self) -> dict[str, str]:
        """Return the environment without the variables that tell git where a repository is."""
        return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}

    def git(self, directory: Path, *arguments: str) -> str:
        """Run git in a directory and return its standard output."""
        command = [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "-c",
            "commit.gpgsign=false",
            "-C",
            str(directory),
            *arguments,
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            check=True,
            env=self.scrubbed_environment(),
            text=True,
        )
        return completed.stdout.strip()

    def make_repository(self) -> Path:
        """Create a repository that holds the baseline documents in one commit."""
        context = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(context.cleanup)
        directory = Path(context.name)
        self.git(directory, "init", "--quiet")
        english, japanese = base_documents()
        files = {
            counts.ENGLISH_DOCUMENT_PATH: english,
            counts.JAPANESE_DOCUMENT_PATH: japanese,
            counts.EXCEPTIONS_PATH: json.dumps(base_exceptions()),
        }
        for relative_path, text in files.items():
            target = directory / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(text.encode("utf-8"))
        self.git(directory, "add", "docs")
        self.git(directory, "commit", "--quiet", "-m", "fixture")
        self.git(directory, "tag", "baseline")
        return directory

    def run_in(self, directory: Path, arguments: list[str]) -> tuple[int, dict]:
        """Run main() with the repository as the working directory and return (exit code, report)."""
        previous = Path.cwd()
        os.chdir(directory)
        self.addCleanup(os.chdir, previous)
        standard_output = io.StringIO()
        with mock.patch.dict(os.environ, self.scrubbed_environment(), clear=True):
            with contextlib.redirect_stdout(standard_output), contextlib.redirect_stderr(io.StringIO()):
                exit_code = counts.main([*arguments, "--json"])
        os.chdir(previous)
        return exit_code, json.loads(standard_output.getvalue())

    def test_rev_is_the_full_sha_for_every_way_of_naming_it(self) -> None:
        """A branch-less `HEAD`, a tag and an abbreviated SHA all resolve to the 40-digit SHA."""
        directory = self.make_repository()
        full_sha = self.git(directory, "rev-parse", "HEAD")
        self.assertRegex(full_sha, r"^[0-9a-f]{40}$")
        for name in ("HEAD", "baseline", full_sha[:7]):
            with self.subTest(name=name):
                exit_code, report = self.run_in(directory, ["--rev", name])
                self.assertEqual(exit_code, 0)
                self.assertEqual(report["source"], {"mode": "rev", "rev": full_sha})
                self.assertRegex(report["source"]["rev"], r"^[0-9a-f]{40}$")

    def test_index_and_worktree_modes_have_no_rev(self) -> None:
        """The other two git modes name their mode and carry no revision."""
        directory = self.make_repository()
        for mode, arguments in (("index", []), ("worktree", ["--worktree"])):
            with self.subTest(mode=mode):
                exit_code, report = self.run_in(directory, arguments)
                self.assertEqual(exit_code, 0)
                self.assertEqual(report["source"], {"mode": mode})

    def test_unknown_revision_is_no_verdict(self) -> None:
        """A name that is not a commit ends the run with exit 2."""
        directory = self.make_repository()
        exit_code, report = self.run_in(directory, ["--rev", "no-such-revision"])
        self.assertEqual(exit_code, 2)
        self.assertEqual(report["verdict"], "no-verdict")


# --------------------------------------------------------------------------------------
# Mistakes of the real reference at commit 806ce0f8, cut down
# --------------------------------------------------------------------------------------


class RecordedMistakeTest(unittest.TestCase):
    """The disagreements that the real reference had are named by the checks, and fixing them silences the checks."""

    def mini_pair(
        self,
        summary_rows: Sequence[tuple[str, int, int, str]],
        english_body: str,
        japanese_body: str,
    ) -> tuple[str, str]:
        """Render an (English, Japanese) pair with no selector commands."""
        return (
            render_document("en", summary_rows, english_body),
            render_document("ja", summary_rows, japanese_body),
        )

    def names(self, count: int) -> list[str]:
        """Return `count` generated command names."""
        return [f"Command{index:02d}" for index in range(1, count + 1)]

    def test_summary_says_twenty_where_the_section_lists_twenty_one(self) -> None:
        """Blueprint: the summary row and the opening totals say 20; 21 commands are listed."""
        prefix = "UAIP.Editor.Blueprint"
        bodies = [
            domain_block(code, prefix, f"### Graph editing{count_label(code, 21)}", self.names(21))
            for code in ("en", "ja")
        ]
        evaluation, _ = run_check(*self.mini_pair([(prefix, 20, 0, "—")], *bodies), no_exceptions())
        self.assertEqual(check_ids(evaluation), {"K1", "K2"})
        k2 = findings_of(evaluation, "K2", "en")
        self.assertEqual([(finding.expected, finding.actual) for finding in k2], [(20, 21)])
        fixed, _ = run_check(*self.mini_pair([(prefix, 21, 0, "—")], *bodies), no_exceptions())
        self.assertEqual(fixed.findings, ())

    def test_counted_heading_whose_table_is_empty(self) -> None:
        """Blueprint: `Asset creation (1)` / `アセット作成（1）` heads an empty table."""
        prefix = "UAIP.Editor.Blueprint"
        titles = {"en": "Asset creation", "ja": "アセット作成"}
        graph = {"en": "Graph", "ja": "グラフ"}
        bodies: list[str] = []
        for code in ("en", "ja"):
            empty = f"### {titles[code]}{count_label(code, 1)}\n\n{table_markdown(code, [])}\n"
            filled = f"### {graph[code]}{count_label(code, 2)}\n\n{table_markdown(code, ['`A`', '`B`'])}\n"
            bodies.append(f"## {prefix}\n\n{empty}\n{filled}")
        evaluation, _ = run_check(*self.mini_pair([(prefix, 2, 0, "—")], *bodies), no_exceptions())
        self.assertEqual(check_ids(evaluation), {"K4"})
        self.assertEqual([finding.language for finding in findings_of(evaluation, "K4")], ["en", "ja"])

    def test_state_tree_heading_counts_thirteen_rows_as_six(self) -> None:
        """StateTree (en): one heading says 6 over 13 rows; two sub-headings that add up fix it."""
        prefix = "UAIP.Editor.StateTree"
        broken = domain_block("en", prefix, "### Global task / evaluator editing (6)", self.names(13))
        japanese = domain_block(
            "ja",
            prefix,
            "### グローバルタスクと評価器の編集（13）",
            self.names(13),
        )
        evaluation, _ = run_check(
            render_document("en", [(prefix, 13, 0, "—")], broken),
            render_document("ja", [(prefix, 13, 0, "—")], japanese),
            no_exceptions(),
        )
        k3 = findings_of(evaluation, "K3")
        self.assertEqual([(finding.language, finding.expected, finding.actual) for finding in k3], [("en", 6, 13)])

    def test_state_tree_with_sub_headings_is_consistent(self) -> None:
        """StateTree: the parent heading without a count and two counted sub-headings."""
        prefix = "UAIP.Editor.StateTree"
        bodies: list[str] = []
        for code in ("en", "ja"):
            tasks = table_markdown(code, [f"`{name}`" for name in self.names(6)])
            evaluators = table_markdown(code, [f"`Evaluator{index}`" for index in range(7)])
            bodies.append(
                f"## {prefix}\n\n### Global editing\n\n#### Tasks{count_label(code, 6)}\n\n{tasks}\n\n"
                f"#### Evaluators{count_label(code, 7)}\n\n{evaluators}\n"
            )
        evaluation, _ = run_check(*self.mini_pair([(prefix, 13, 0, "—")], *bodies), no_exceptions())
        self.assertEqual(evaluation.findings, ())

    def test_chaos_cloth_asset_counted_in_one_language_only(self) -> None:
        """ChaosClothAsset: Japanese puts the commands under (6), English under no count; K5 names each of them."""
        prefix = "UAIP.Editor.ChaosClothAsset"
        english = domain_block("en", prefix, "### Cloth editing", self.names(6))
        japanese = domain_block("ja", prefix, f"### クロスの編集{count_label('ja', 6)}", self.names(6))
        # A counted heading must exist somewhere, or the pair would have nothing to check.
        other = "UAIP.Editor.Other"
        english += "\n" + domain_block("en", other, f"### Things{count_label('en', 1)}", ["Only"])
        japanese += "\n" + domain_block("ja", other, f"### もの{count_label('ja', 1)}", ["Only"])
        evaluation, _ = run_check(
            *self.mini_pair([(prefix, 6, 0, "—"), (other, 1, 0, "—")], english, japanese),
            no_exceptions(),
        )
        self.assertEqual(check_ids(evaluation), {"K5"})
        found = findings_of(evaluation, "K5")
        self.assertEqual(len(found), 6)
        self.assertEqual({(finding.domain, finding.expected, finding.actual) for finding in found}, {(prefix, None, 6)})

    def test_demo_column_of_runtime_domains(self) -> None:
        """Runtime.World, Runtime.AI and Runtime.Animation: the Demo column does not match the marks."""
        domains = [
            ("UAIP.Runtime.World", 4, 2, "—", "partial (2/4)"),
            ("UAIP.Runtime.AI", 14, 12, "partial (13/14)", "partial (12/14)"),
            ("UAIP.Runtime.Animation", 7, 5, "partial (6/7)", "partial (5/7)"),
        ]
        bodies: dict[str, str] = {}
        for code in ("en", "ja"):
            blocks = [
                domain_block(code, prefix, f"### Commands{count_label(code, native)}", self.names(native), marked)
                for prefix, native, marked, _, _ in domains
            ]
            bodies[code] = "\n".join(blocks)
        broken_summary = [(prefix, native, 0, written) for prefix, native, _, written, _ in domains]
        fixed_summary = [(prefix, native, 0, corrected) for prefix, native, _, _, corrected in domains]
        evaluation, _ = run_check(
            *self.mini_pair(broken_summary, bodies["en"], bodies["ja"]),
            no_exceptions(),
        )
        self.assertEqual(check_ids(evaluation), {"K7"})
        reported = {finding.domain for finding in findings_of(evaluation, "K7")}
        self.assertEqual(reported, {prefix for prefix, *_ in domains})
        ai = [finding for finding in findings_of(evaluation, "K7", "en") if finding.domain == "UAIP.Runtime.AI"]
        ai_values = [(finding.expected, finding.actual) for finding in ai]
        self.assertEqual(ai_values, [("partial (12/14)", "partial (13/14)")])
        fixed, _ = run_check(
            *self.mini_pair(fixed_summary, bodies["en"], bodies["ja"]),
            no_exceptions(),
        )
        self.assertEqual(fixed.findings, ())


if __name__ == "__main__":
    unittest.main()
