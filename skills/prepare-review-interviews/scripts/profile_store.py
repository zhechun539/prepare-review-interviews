#!/usr/bin/env python3
"""Persist interview-candidate profiles and session summaries locally."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


PROFILE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def state_root() -> Path:
    override = os.environ.get("INTERVIEW_PREP_STATE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return (Path.home() / ".codex" / "interview-prep-review").resolve()


def profile_dir(profile_id: str) -> Path:
    if not PROFILE_ID_RE.fullmatch(profile_id):
        raise ValueError("profile id must match [a-z0-9][a-z0-9_-]{0,63}")
    return state_root() / "profiles" / profile_id


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temp.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_record(raw_path: str) -> dict:
    path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"source not found: {path}")
    stat = path.stat()
    return {
        "name": path.name,
        "path": str(path),
        "size": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
        "sha256": sha256(path),
    }


def command_status(args: argparse.Namespace) -> int:
    directory = profile_dir(args.profile_id)
    profile = directory / "profile.json"
    manifest = directory / "sources.json"
    if not profile.is_file():
        result = {"status": "missing", "profile_id": args.profile_id, "state_dir": str(directory)}
    else:
        data = read_json(profile)
        sources = read_json(manifest).get("sources", []) if manifest.is_file() else []
        missing_sources = []
        changed_sources = []
        for item in sources:
            raw_path = item.get("path")
            if not raw_path:
                continue
            source_path = Path(raw_path)
            if not source_path.is_file():
                missing_sources.append(raw_path)
                continue
            stat = source_path.stat()
            current_modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds")
            if stat.st_size != item.get("size") or current_modified != item.get("modified_at"):
                changed_sources.append(raw_path)
        result = {
            "status": "stale" if missing_sources or changed_sources else "ready",
            "profile_id": args.profile_id,
            "updated_at": data.get("updated_at"),
            "source_count": len(sources),
            "missing_source_count": len(missing_sources),
            "changed_source_count": len(changed_sources),
            "missing_sources": missing_sources,
            "changed_sources": changed_sources,
            "state_dir": str(directory),
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_show(args: argparse.Namespace) -> int:
    path = profile_dir(args.profile_id) / "profile.json"
    if not path.is_file():
        print(f"profile missing: {path}", file=sys.stderr)
        return 2
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def command_save(args: argparse.Namespace) -> int:
    input_path = Path(args.input).expanduser().resolve()
    profile = read_json(input_path)
    profile["schema_version"] = profile.get("schema_version", 1)
    profile["updated_at"] = utc_now()
    directory = profile_dir(args.profile_id)
    source_paths = list(args.source or [])
    if args.source_list:
        source_list_path = Path(args.source_list).expanduser().resolve()
        with source_list_path.open("r", encoding="utf-8") as handle:
            listed = json.load(handle)
        if not isinstance(listed, list) or not all(isinstance(item, str) for item in listed):
            raise ValueError("source list JSON must be an array of path strings")
        source_paths.extend(listed)
    existing_manifest_path = directory / "sources.json"
    existing_sources = read_json(existing_manifest_path).get("sources", []) if existing_manifest_path.is_file() else []
    merged_sources = {item.get("path"): item for item in existing_sources if item.get("path")}
    for item in source_paths:
        record = source_record(item)
        merged_sources[record["path"]] = record
    sources = sorted(merged_sources.values(), key=lambda item: item["path"].casefold())
    write_json_atomic(directory / "profile.json", profile)
    write_json_atomic(directory / "sources.json", {"updated_at": utc_now(), "sources": sources})
    print(json.dumps({"status": "saved", "profile_id": args.profile_id, "source_count": len(sources), "state_dir": str(directory)}, ensure_ascii=False, indent=2))
    return 0


def command_record(args: argparse.Namespace) -> int:
    input_path = Path(args.input).expanduser().resolve()
    payload = read_json(input_path)
    directory = profile_dir(args.profile_id)
    if not (directory / "profile.json").is_file():
        print("create the profile before recording sessions", file=sys.stderr)
        return 2
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    payload["recorded_at"] = utc_now()
    payload["mode"] = args.mode
    destination = directory / "sessions" / f"{timestamp}-{args.mode}.json"
    write_json_atomic(destination, payload)
    print(json.dumps({"status": "recorded", "path": str(destination)}, ensure_ascii=False, indent=2))
    return 0


def command_delete(args: argparse.Namespace) -> int:
    directory = profile_dir(args.profile_id)
    if not args.confirm or args.confirm != args.profile_id:
        print("refusing deletion: --confirm must exactly match --profile-id", file=sys.stderr)
        return 2
    if directory.is_dir():
        shutil.rmtree(directory)
    print(json.dumps({"status": "deleted", "profile_id": args.profile_id, "path": str(directory)}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "show"):
        child = subparsers.add_parser(name)
        child.add_argument("--profile-id", default="default")
        child.set_defaults(func=command_status if name == "status" else command_show)
    save = subparsers.add_parser("save")
    save.add_argument("--profile-id", default="default")
    save.add_argument("--input", required=True)
    save.add_argument("--source", action="append")
    save.add_argument("--source-list", help="UTF-8 JSON array of source paths")
    save.set_defaults(func=command_save)
    record = subparsers.add_parser("record")
    record.add_argument("--profile-id", default="default")
    record.add_argument("--mode", choices=("prep", "review"), required=True)
    record.add_argument("--input", required=True)
    record.set_defaults(func=command_record)
    delete = subparsers.add_parser("delete")
    delete.add_argument("--profile-id", default="default")
    delete.add_argument("--confirm", required=True)
    delete.set_defaults(func=command_delete)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
