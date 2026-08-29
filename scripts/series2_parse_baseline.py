#!/usr/bin/env python3
"""Measure the series-2 interpreter parse baseline from released eval logs.

This script is deliberately standard-library-only on Python 3.14+. On older
Python versions, install ``zipfile-zstd`` as described in docs/RELEASE.md.

It reads the two manifest-pinned series-2 eval payloads without modifying
them, verifies their identities and expected episode coverage, then emits:

* released-log and episode inventory, including execution/data gaps;
* action-record totals and rejection-reason census;
* hard parse-failure, explicit-unmappable, and combined rates;
* the historical F9 rate denominator; and
* a deterministic per-episode breakdown.

Usage:
    python scripts/series2_parse_baseline.py
    python scripts/series2_parse_baseline.py --json
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

try:
    import zipfile_zstd  # noqa: F401  (Python <3.14 compatibility shim)
except ImportError:
    pass
import zipfile


RUN_REVISION = "da8c140"
HARD_PARSE_REASON = "unparseable_proposal"
EXPLICIT_UNMAPPABLE_REASON = "unmappable_action"
TRUNCATED_PLAYER_REASON = "truncated_output"

ANCHOR_IDS = tuple(f"lu-70000{i}" for i in range(4))
SOLVABLE_GRID_IDS = tuple(f"lu-90000{i}" for i in range(6))
GRID_IDS = tuple(
    item
    for index in range(6)
    for item in (f"lu-90000{index}", f"lu-90000{index}u")
)

RELEASE_CELLS: tuple[dict[str, Any], ...] = (
    {
        "name": "s2-main",
        "path": (
            "logs/s2-main/"
            "2026-07-09T01-35-19-00-00_latent-underground_"
            "FKN5sJryQnRmScaMNZWBWX.eval"
        ),
        "sha256": "cf0cf5782d2a44e23642af8528f0ee96ecc90e56aa90947d8b69bce20d29752f",
        "disclose_win": False,
        "sample_ids": ANCHOR_IDS + GRID_IDS,
        "epochs": 10,
    },
    {
        "name": "s2-disclosure",
        "path": (
            "logs/s2-disclosure/"
            "2026-07-09T15-40-57-00-00_latent-underground_"
            "9TdVXCiMv2j3um7YaphVrG.eval"
        ),
        "sha256": "7f7ed0b4ecb9f015f5459e4768aed4acd43bb543ac48a2fcb35d3df4bd6d9657",
        "disclose_win": True,
        "sample_ids": SOLVABLE_GRID_IDS,
        "epochs": 10,
    },
)

DUPLICATE_COPIES: tuple[dict[str, str], ...] = (
    {
        "canonical_cell": "s2-disclosure",
        "path": "logs/s2-disclosure/closed-copy.eval",
        "sha256": "7f7ed0b4ecb9f015f5459e4768aed4acd43bb543ac48a2fcb35d3df4bd6d9657",
    },
)

DEFINITIONS: dict[str, str] = {
    "hard_parse_failure": (
        "Exact rejection_reason 'unparseable_proposal': series-2 "
        "parse_proposal returned None after no exact uppercase UNMAPPABLE "
        "substring was found and JSON extraction, decoding, or OpProposal "
        "schema validation failed. This was the F9 parse-failure numerator."
    ),
    "explicit_unmappable": (
        "Exact rejection_reason 'unmappable_action': parse_proposal returned "
        "OpProposal(op=UNMAPPABLE) after seeing the exact uppercase substring "
        "UNMAPPABLE. Series 2 treated this as interpreter abstention/friction, "
        "not a hard parse failure."
    ),
    "non_executable_interpretation": (
        "Union of hard_parse_failure and explicit_unmappable. This is a "
        "sensitivity count, not a historical series-2 parser category."
    ),
    "all_action_denominator": (
        "Every game_log.ops record in the selected episode scope."
    ),
    "historical_f9_denominator": (
        "All game_log.ops records in the selected episode scope except exact "
        "unmappable_action records and exact truncated_output records. Series "
        "2 excluded explicit UNMAPPABLE from its rate denominator, while "
        "truncated player output bypassed the interpreter."
    ),
    "completed_episode_scope": (
        "Episodes with no recorded sample error and a nonempty engine terminal "
        "state. All released episodes remain inventoried and measured in the "
        "all_released scope."
    ),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rate_record(count: int, denominator: int) -> dict[str, Any]:
    if denominator == 0:
        return {
            "count": count,
            "denominator": denominator,
            "fraction": f"{count}/{denominator}",
            "rate": None,
            "percent": None,
        }
    value = count / denominator
    return {
        "count": count,
        "denominator": denominator,
        "fraction": f"{count}/{denominator}",
        "rate": f"{value:.12f}",
        "percent": f"{value * 100:.8f}",
    }


def action_summary(episodes: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(episodes)
    total_actions = sum(row["action_records"] for row in rows)
    hard = sum(row["hard_parse_failure"] for row in rows)
    unmappable = sum(row["explicit_unmappable"] for row in rows)
    combined = hard + unmappable
    truncated = sum(row["truncated_output"] for row in rows)
    f9_denominator = sum(row["historical_f9_denominator"] for row in rows)
    parsed_engine_rejections = sum(
        row["parsed_engine_rejections"] for row in rows
    )
    reasons: collections.Counter[str] = collections.Counter()
    for row in rows:
        reasons.update(row["rejection_reasons"])

    return {
        "episodes": len(rows),
        "total_actions": total_actions,
        "counts": {
            "hard_parse_failure": hard,
            "explicit_unmappable": unmappable,
            "non_executable_interpretation": combined,
            "truncated_output": truncated,
            "parsed_engine_rejections": parsed_engine_rejections,
        },
        "denominators": {
            "all_actions": total_actions,
            "historical_f9": f9_denominator,
        },
        "rates": {
            "hard_parse_failure_all_actions": rate_record(hard, total_actions),
            "hard_parse_failure_historical_f9": rate_record(
                hard, f9_denominator
            ),
            "explicit_unmappable_all_actions": rate_record(
                unmappable, total_actions
            ),
            "non_executable_interpretation_all_actions": rate_record(
                combined, total_actions
            ),
        },
        "rejection_reasons": dict(sorted(reasons.items())),
    }


def error_summary(error: Any) -> str | None:
    if not error:
        return None
    if isinstance(error, dict):
        error_type = error.get("type") or error.get("name") or "error"
        message = error.get("message") or error.get("detail")
        if message:
            return f"{error_type}: {message}"
        return json.dumps(error, sort_keys=True, ensure_ascii=False)
    return str(error)


def parse_episode(
    cell_name: str,
    member: str,
    sample: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    sample_id = sample.get("id")
    epoch = sample.get("epoch")
    sample_error = sample.get("error")

    store = sample.get("store")
    if not isinstance(store, dict):
        store = {}
        issues.append("missing_or_invalid_store")
    game_log = store.get("game_log")
    if not isinstance(game_log, dict):
        game_log = {}
        issues.append("missing_or_invalid_game_log")
    ops = game_log.get("ops")
    if not isinstance(ops, list):
        ops = []
        issues.append("missing_or_invalid_ops")

    reasons: collections.Counter[str] = collections.Counter()
    hard = 0
    unmappable = 0
    truncated = 0
    parsed_engine_rejections = 0
    bad_op_records = 0
    classification_shape_mismatches = 0
    observed_turns: list[Any] = []

    for op in ops:
        if not isinstance(op, dict):
            bad_op_records += 1
            reasons["<invalid-op-record>"] += 1
            continue
        reason = op.get("rejection_reason")
        proposed = op.get("dm_proposed_op")
        validated = op.get("engine_validated_op")
        reason_key = "<accepted>" if reason is None else str(reason)
        reasons[reason_key] += 1
        observed_turns.append(op.get("turn"))
        if reason == HARD_PARSE_REASON:
            hard += 1
            if proposed != {} or validated is not None:
                classification_shape_mismatches += 1
        elif reason == EXPLICIT_UNMAPPABLE_REASON:
            unmappable += 1
            if (
                not isinstance(proposed, dict)
                or proposed.get("op") != "UNMAPPABLE"
                or validated is not None
            ):
                classification_shape_mismatches += 1
        elif reason == TRUNCATED_PLAYER_REASON:
            truncated += 1
            if proposed != {} or validated is not None:
                classification_shape_mismatches += 1
        elif reason is not None:
            parsed_engine_rejections += 1

    action_records = len(ops)
    historical_f9_denominator = action_records - unmappable - truncated
    terminal = game_log.get("terminal")
    completed = not bool(sample_error) and bool(terminal)

    turns = game_log.get("turns")
    if turns != action_records:
        issues.append(f"turn_count_mismatch:{turns!r}!={action_records}")
    expected_turns = list(range(1, action_records + 1))
    if bad_op_records:
        issues.append(f"invalid_op_records:{bad_op_records}")
    elif observed_turns != expected_turns:
        issues.append("non_contiguous_op_turns")
    if classification_shape_mismatches:
        issues.append(
            "classification_shape_mismatches:"
            f"{classification_shape_mismatches}"
        )
    if game_log.get("instance_id") not in (None, sample_id):
        issues.append(
            "instance_id_mismatch:"
            f"{game_log.get('instance_id')!r}!={sample_id!r}"
        )
    if sample_error:
        issues.append("sample_error")
    if not terminal:
        issues.append("nonterminal_game_log")

    combined = hard + unmappable
    rates = {
        "hard_parse_failure_all_actions": rate_record(hard, action_records),
        "hard_parse_failure_historical_f9": rate_record(
            hard, historical_f9_denominator
        ),
        "explicit_unmappable_all_actions": rate_record(
            unmappable, action_records
        ),
        "non_executable_interpretation_all_actions": rate_record(
            combined, action_records
        ),
    }

    return {
        "cell": cell_name,
        "member": member,
        "sample_id": sample_id,
        "epoch": epoch,
        "completed": completed,
        "terminal": terminal,
        "sample_error_present": bool(sample_error),
        "sample_error_summary": error_summary(sample_error),
        "action_records": action_records,
        "hard_parse_failure": hard,
        "explicit_unmappable": unmappable,
        "non_executable_interpretation": combined,
        "truncated_output": truncated,
        "parsed_engine_rejections": parsed_engine_rejections,
        "historical_f9_denominator": historical_f9_denominator,
        "rejection_reasons": dict(sorted(reasons.items())),
        "rates": rates,
        "issues": issues,
    }


def episode_key(row: dict[str, Any]) -> tuple[Any, Any]:
    return row.get("sample_id"), row.get("epoch")


def load_cell(repo_root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    path = repo_root / spec["path"]
    if not path.is_file():
        raise FileNotFoundError(f"missing released log: {path}")

    actual_hash = sha256_file(path)
    if actual_hash != spec["sha256"]:
        raise ValueError(
            f"released-log hash mismatch for {path}: "
            f"expected {spec['sha256']}, got {actual_hash}"
        )

    try:
        with zipfile.ZipFile(path) as archive:
            header = json.loads(archive.read("header.json"))
            sample_members = sorted(
                name
                for name in archive.namelist()
                if name.startswith("samples/") and name.endswith(".json")
            )
            episodes = [
                parse_episode(
                    spec["name"], member, json.loads(archive.read(member))
                )
                for member in sample_members
            ]
    except NotImplementedError as exc:
        raise RuntimeError(
            "this Python cannot read ZIP_ZSTANDARD eval members; use Python "
            "3.14+ or install zipfile-zstd"
        ) from exc

    episodes.sort(
        key=lambda row: (
            str(row.get("sample_id")),
            int(row.get("epoch")) if isinstance(row.get("epoch"), int) else -1,
            row.get("member", ""),
        )
    )

    expected_keys = {
        (sample_id, epoch)
        for sample_id in spec["sample_ids"]
        for epoch in range(1, spec["epochs"] + 1)
    }
    observed_counter = collections.Counter(episode_key(row) for row in episodes)
    observed_keys = set(observed_counter)
    missing = sorted(expected_keys - observed_keys)
    unexpected = sorted(observed_keys - expected_keys, key=lambda key: str(key))
    duplicates = sorted(
        (key, count) for key, count in observed_counter.items() if count > 1
    )

    eval_block = header.get("eval") or {}
    revision = (eval_block.get("revision") or {}).get("commit")
    task_args = eval_block.get("task_args") or {}
    config = eval_block.get("config") or {}
    dataset = eval_block.get("dataset") or {}
    header_issues: list[str] = []
    provenance_notes: list[str] = []
    if header.get("status") != "success":
        header_issues.append(f"header_status:{header.get('status')!r}")
    if revision != RUN_REVISION:
        header_issues.append(f"revision:{revision!r}!={RUN_REVISION!r}")
    if task_args.get("disclose_win") is not spec["disclose_win"]:
        header_issues.append(
            "disclose_win:"
            f"{task_args.get('disclose_win')!r}!={spec['disclose_win']!r}"
        )
    if config.get("epochs") != spec["epochs"]:
        header_issues.append(
            f"epochs:{config.get('epochs')!r}!={spec['epochs']!r}"
        )
    if tuple(dataset.get("sample_ids") or ()) != tuple(spec["sample_ids"]):
        header_issues.append("header_sample_ids_do_not_match_release_spec")
    if (eval_block.get("revision") or {}).get("dirty"):
        provenance_notes.append(
            "eval header records dirty=true; the exact uncommitted source "
            "diff is not embedded in the eval payload"
        )

    completed = [row for row in episodes if row["completed"]]
    execution_gaps = [row for row in episodes if not row["completed"]]
    data_issue_episodes = [row for row in episodes if row["issues"]]
    fatal_data_issues = [
        row
        for row in episodes
        if any(
            issue
            in {
                "missing_or_invalid_store",
                "missing_or_invalid_game_log",
                "missing_or_invalid_ops",
            }
            or issue.startswith("classification_shape_mismatches:")
            for issue in row["issues"]
        )
    ]

    return {
        "cell": spec["name"],
        "log": spec["path"],
        "sha256": actual_hash,
        "header": {
            "status": header.get("status"),
            "revision": revision,
            "dirty": (eval_block.get("revision") or {}).get("dirty"),
            "created": eval_block.get("created"),
            "epochs": config.get("epochs"),
            "dataset_samples_before_filter": dataset.get("samples"),
            "sample_ids": dataset.get("sample_ids"),
            "disclose_win": task_args.get("disclose_win"),
            "header_issues": header_issues,
            "provenance_notes": provenance_notes,
        },
        "inventory": {
            "expected_episodes": len(expected_keys),
            "observed_episode_records": len(episodes),
            "completed_episodes": len(completed),
            "execution_gap_episodes": len(execution_gaps),
            "missing_episode_keys": [list(key) for key in missing],
            "unexpected_episode_keys": [list(key) for key in unexpected],
            "duplicate_episode_keys": [
                {"key": list(key), "count": count}
                for key, count in duplicates
            ],
            "data_issue_episodes": len(data_issue_episodes),
            "fatal_data_issue_episodes": len(fatal_data_issues),
        },
        "metrics": {
            "all_released": action_summary(episodes),
            "completed_episodes": action_summary(completed),
        },
        "execution_gaps": [
            {
                "sample_id": row["sample_id"],
                "epoch": row["epoch"],
                "terminal": row["terminal"],
                "sample_error_summary": row["sample_error_summary"],
                "action_records": row["action_records"],
                "issues": row["issues"],
            }
            for row in execution_gaps
        ],
        "episodes": episodes,
    }


def parse_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        digest, relative = parts
        entries[relative.replace("\\", "/")] = digest.lower()
    return entries


def release_integrity(repo_root: Path) -> dict[str, Any]:
    manifest_path = repo_root / "MANIFEST.sha256"
    issues: list[str] = []
    manifest_entries: dict[str, str] = {}
    if manifest_path.is_file():
        manifest_entries = parse_manifest(manifest_path)
    else:
        issues.append("missing MANIFEST.sha256")

    for spec in RELEASE_CELLS:
        manifest_hash = manifest_entries.get(spec["path"])
        if manifest_hash != spec["sha256"]:
            issues.append(
                f"manifest entry for {spec['path']}: "
                f"{manifest_hash!r} != {spec['sha256']!r}"
            )

    duplicates: list[dict[str, Any]] = []
    for duplicate in DUPLICATE_COPIES:
        path = repo_root / duplicate["path"]
        manifest_hash = manifest_entries.get(duplicate["path"])
        if manifest_hash != duplicate["sha256"]:
            issues.append(
                f"manifest entry for {duplicate['path']}: "
                f"{manifest_hash!r} != {duplicate['sha256']!r}"
            )
        if path.is_file():
            actual_hash = sha256_file(path)
            present = True
            identical = actual_hash == duplicate["sha256"]
            if not identical:
                issues.append(
                    f"duplicate-copy hash mismatch for {duplicate['path']}: "
                    f"{actual_hash}"
                )
        else:
            actual_hash = None
            present = False
            identical = None
        duplicates.append(
            {
                **duplicate,
                "present": present,
                "actual_sha256": actual_hash,
                "identical_to_canonical": identical,
                "aggregated": False,
            }
        )

    return {
        "manifest": "MANIFEST.sha256",
        "issues": issues,
        "duplicate_copies": duplicates,
    }


RATE_NAMES = (
    "hard_parse_failure_all_actions",
    "hard_parse_failure_historical_f9",
    "explicit_unmappable_all_actions",
    "non_executable_interpretation_all_actions",
)


def maximum_rates(cells: list[dict[str, Any]]) -> dict[str, Any]:
    maxima: dict[str, Any] = {}
    for scope in ("all_released", "completed_episodes"):
        maxima[scope] = {}
        for rate_name in RATE_NAMES:
            candidates: list[tuple[Fraction, str, dict[str, Any]]] = []
            for cell in cells:
                record = cell["metrics"][scope]["rates"][rate_name]
                if record["denominator"]:
                    candidates.append(
                        (
                            Fraction(record["count"], record["denominator"]),
                            cell["cell"],
                            record,
                        )
                    )
            if not candidates:
                maxima[scope][rate_name] = None
                continue
            maximum = max(item[0] for item in candidates)
            tied = [item for item in candidates if item[0] == maximum]
            maxima[scope][rate_name] = {
                "cells": [item[1] for item in tied],
                **tied[0][2],
            }
    return maxima


def format_rate(record: dict[str, Any]) -> str:
    if record["rate"] is None:
        return f"{record['fraction']} = NA"
    return (
        f"{record['fraction']} = {record['rate']} "
        f"({record['percent']}%)"
    )


def print_text(report: dict[str, Any]) -> None:
    print("SERIES-2 UNPARSEABLE-ACTION BASELINE")
    print(f"run-bound revision: {report['run_revision']}")
    print("\nDEFINITIONS (frozen before measurement)")
    for name, definition in report["definitions"].items():
        print(f"  {name}: {definition}")

    print("\nRELEASE INTEGRITY")
    integrity = report["release_integrity"]
    print(f"  manifest: {integrity['manifest']}")
    print(f"  issues: {len(integrity['issues'])}")
    for issue in integrity["issues"]:
        print(f"    - {issue}")
    for duplicate in integrity["duplicate_copies"]:
        print(
            "  duplicate copy: "
            f"{duplicate['path']} present={duplicate['present']} "
            f"identical={duplicate['identical_to_canonical']} "
            "aggregated=False"
        )

    for cell in report["cells"]:
        inventory = cell["inventory"]
        print(f"\nCELL {cell['cell']}")
        print(f"  log: {cell['log']}")
        print(f"  sha256: {cell['sha256']}")
        print(
            "  header: "
            f"status={cell['header']['status']} "
            f"revision={cell['header']['revision']} "
            f"dirty={cell['header']['dirty']} "
            f"created={cell['header']['created']}"
        )
        print(
            "  episodes: "
            f"expected={inventory['expected_episodes']} "
            f"observed={inventory['observed_episode_records']} "
            f"completed={inventory['completed_episodes']} "
            f"execution_gaps={inventory['execution_gap_episodes']}"
        )
        print(
            "  coverage: "
            f"missing={len(inventory['missing_episode_keys'])} "
            f"unexpected={len(inventory['unexpected_episode_keys'])} "
            f"duplicates={len(inventory['duplicate_episode_keys'])} "
            f"fatal_data_issues={inventory['fatal_data_issue_episodes']}"
        )
        for note in cell["header"]["provenance_notes"]:
            print(f"    provenance note: {note}")
        for gap in cell["execution_gaps"]:
            print(
                "    execution gap: "
                f"{gap['sample_id']} ep{gap['epoch']} "
                f"terminal={gap['terminal']!r} actions={gap['action_records']} "
                f"error={gap['sample_error_summary']!r}"
            )

        for scope in ("all_released", "completed_episodes"):
            summary = cell["metrics"][scope]
            print(
                f"  {scope}: episodes={summary['episodes']} "
                f"total_actions={summary['total_actions']}"
            )
            for rate_name in RATE_NAMES:
                print(
                    f"    {rate_name}: "
                    f"{format_rate(summary['rates'][rate_name])}"
                )
            print(
                "    rejection_reasons: "
                f"{json.dumps(summary['rejection_reasons'], sort_keys=True)}"
            )

    print("\nMAXIMUM PER-CELL RATES (descriptive; no threshold selected)")
    for scope, rate_map in report["maximum_per_cell_rates"].items():
        print(f"  {scope}:")
        for rate_name, record in rate_map.items():
            if record is None:
                print(f"    {rate_name}: NA")
            else:
                print(
                    f"    {rate_name}: cells={','.join(record['cells'])} "
                    f"{format_rate(record)}"
                )

    print("\nPER-EPISODE BREAKDOWN")
    print(
        "  cell sample_id epoch completed terminal actions hard_parse "
        "explicit_unmappable combined truncated f9_denominator "
        "hard/all hard/f9 unmappable/all combined/all issues"
    )
    for cell in report["cells"]:
        for row in cell["episodes"]:
            rates = row["rates"]
            print(
                f"  {row['cell']} {row['sample_id']} {row['epoch']} "
                f"{str(row['completed']).lower()} {row['terminal'] or '-'} "
                f"{row['action_records']} {row['hard_parse_failure']} "
                f"{row['explicit_unmappable']} "
                f"{row['non_executable_interpretation']} "
                f"{row['truncated_output']} "
                f"{row['historical_f9_denominator']} "
                f"{rates['hard_parse_failure_all_actions']['fraction']} "
                f"{rates['hard_parse_failure_historical_f9']['fraction']} "
                f"{rates['explicit_unmappable_all_actions']['fraction']} "
                f"{rates['non_executable_interpretation_all_actions']['fraction']} "
                f"{','.join(row['issues']) or '-'}"
            )


def has_fatal_measurement_gap(report: dict[str, Any]) -> bool:
    if report["release_integrity"]["issues"]:
        return True
    for cell in report["cells"]:
        inventory = cell["inventory"]
        if cell["header"]["header_issues"]:
            return True
        if inventory["missing_episode_keys"]:
            return True
        if inventory["unexpected_episode_keys"]:
            return True
        if inventory["duplicate_episode_keys"]:
            return True
        if inventory["fatal_data_issue_episodes"]:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit deterministic JSON instead of the text report",
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    try:
        integrity = release_integrity(repo_root)
        cells = [load_cell(repo_root, spec) for spec in RELEASE_CELLS]
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError,
            zipfile.BadZipFile, RuntimeError) as exc:
        print(f"MEASUREMENT STOPPED: {exc}", file=sys.stderr)
        return 2

    report = {
        "schema_version": 1,
        "run_revision": RUN_REVISION,
        "definitions": DEFINITIONS,
        "release_integrity": integrity,
        "cells": cells,
        "maximum_per_cell_rates": maximum_rates(cells),
    }

    if args.json:
        json.dump(report, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
        print()
    else:
        print_text(report)

    if has_fatal_measurement_gap(report):
        print(
            "MEASUREMENT INCOMPLETE: fatal release/header/data coverage gap; "
            "see inventory above.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
