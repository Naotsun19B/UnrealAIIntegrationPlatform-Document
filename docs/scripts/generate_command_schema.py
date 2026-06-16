#!/usr/bin/env python3
"""Generate a JSON dump of every UAIP command schema.

Connects to a running UE editor via the UAIP HTTP transport, enumerates all
registered commands with `ListCommands`, fetches the full schema for each
via `DescribeCommand`, and writes the combined result to a JSON file.

Output shape:

    {
      "generatedAt": "2026-06-17T12:34:56Z",
      "uaipVersion": "1.0.0",
      "engineVersion": "5.8.0",
      "commandCount": 735,
      "commands": [
        {
          "name": "UAIP.Core.HealthCheck",
          "providerName": "UAIP.Core",
          "description": "...",
          "requiredCapabilities": [],
          "isReadOnly": true,
          "available": true,
          "stability": "Stable",
          "parameterSchema": { ... }
        },
        ...
      ]
    }

Requirements:
- UE editor must be running with `-uaip-http-enable`
- Python 3.10+
- `requests` (`pip install requests`)

Usage:
    python generate_command_schema.py \
        --host http://127.0.0.1:8765 \
        --token-file /path/to/Saved/UAIP/EditorHttpAuthToken.txt \
        --out commands-schema.json

If --token-file is omitted, the script reads UAIP_HTTP_TOKEN from the
environment. Pass --no-auth if the editor was launched with
-uaip-http-no-auth.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("error: this script requires the 'requests' package.", file=sys.stderr)
    print("       pip install requests", file=sys.stderr)
    sys.exit(2)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--host", default="http://127.0.0.1:8765",
                   help="UAIP HTTP base URL (default: http://127.0.0.1:8765)")
    p.add_argument("--token-file", type=Path, default=None,
                   help="Path to EditorHttpAuthToken.txt (overrides --no-auth)")
    p.add_argument("--no-auth", action="store_true",
                   help="Skip the Authorization header (editor launched with -uaip-http-no-auth)")
    p.add_argument("--out", type=Path, default=Path("commands-schema.json"),
                   help="Output JSON path (default: ./commands-schema.json)")
    p.add_argument("--split-by-provider", action="store_true",
                   help="Also emit per-provider files into a sibling 'by-provider/' folder")
    p.add_argument("--include-unavailable", action="store_true",
                   help="Include commands that are Available=false (e.g. optional plugin not loaded)")
    return p.parse_args()


def load_token(args: argparse.Namespace) -> str | None:
    if args.no_auth:
        return None
    if args.token_file:
        return args.token_file.read_text(encoding="utf-8").strip()
    env_token = os.environ.get("UAIP_HTTP_TOKEN")
    if env_token:
        return env_token
    print("error: no Bearer token supplied. Pass --token-file <path>, set", file=sys.stderr)
    print("       UAIP_HTTP_TOKEN, or pass --no-auth.", file=sys.stderr)
    sys.exit(2)


def build_session(token: str | None) -> requests.Session:
    s = requests.Session()
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    s.headers["Content-Type"] = "application/json"
    return s


def execute(s: requests.Session, host: str, command: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {"CommandName": command, "Params": params or {}}
    r = s.post(f"{host}/uaip/commands", json=payload, timeout=120)
    r.raise_for_status()
    body = r.json()
    if not body.get("Success"):
        raise RuntimeError(f"{command} failed: {body.get('ErrorCode')} - {body.get('ErrorMessage')}")
    return body.get("Data", {}) or {}


def main() -> int:
    args = parse_args()
    token = load_token(args)
    session = build_session(token)

    print(f"[1/3] Connecting to {args.host} ...", file=sys.stderr)
    sys_info = execute(session, args.host, "UAIP.Core.GetSystemInfo")
    uaip_version = sys_info.get("UAIPVersion", "unknown")
    engine_version = sys_info.get("EngineVersion", "unknown")
    print(f"      Editor reports UAIP {uaip_version}, UE {engine_version}", file=sys.stderr)

    print("[2/3] Listing commands ...", file=sys.stderr)
    list_data = execute(session, args.host, "UAIP.Core.ListCommands",
                        {"IncludeUnavailable": args.include_unavailable})
    commands = list_data.get("Commands", []) or list_data.get("commands", [])
    print(f"      Found {len(commands)} commands", file=sys.stderr)

    print("[3/3] Describing each command ...", file=sys.stderr)
    schemas = []
    started = time.time()
    for index, entry in enumerate(commands, start=1):
        name = entry.get("Name") or entry.get("name")
        if not name:
            continue
        try:
            data = execute(session, args.host, "UAIP.Core.DescribeCommand", {"CommandName": name})
        except RuntimeError as ex:
            print(f"      [skip] {name}: {ex}", file=sys.stderr)
            continue
        # Some servers nest the descriptor under "Result"; flatten if so.
        descriptor = data.get("Result") if "Result" in data else data
        schemas.append(descriptor)
        if index % 25 == 0 or index == len(commands):
            elapsed = time.time() - started
            print(f"      {index}/{len(commands)}  ({elapsed:.1f}s)", file=sys.stderr)

    payload = {
        "generatedAt": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "uaipVersion": uaip_version,
        "engineVersion": engine_version,
        "commandCount": len(schemas),
        "commands": schemas,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out} ({args.out.stat().st_size:,} bytes, {len(schemas)} commands)", file=sys.stderr)

    if args.split_by_provider:
        by_provider_root = args.out.parent / "by-provider"
        by_provider_root.mkdir(parents=True, exist_ok=True)
        groups: dict[str, list[dict[str, Any]]] = {}
        for descriptor in schemas:
            name = descriptor.get("Name") or descriptor.get("name", "")
            provider = name.rsplit(".", 1)[0] if "." in name else "_misc"
            groups.setdefault(provider, []).append(descriptor)
        for provider, items in groups.items():
            slug = provider.replace(".", "_")
            (by_provider_root / f"{slug}.json").write_text(
                json.dumps({"provider": provider, "commands": items}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        print(f"Wrote {len(groups)} per-provider files to {by_provider_root}/", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
