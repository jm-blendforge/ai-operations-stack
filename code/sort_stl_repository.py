#!/usr/bin/env python3
"""
Blackforge STL repository sorter.

Runs on the operator's machine. Files licensed design downloads into a clean,
offline, per-designer/per-product library and keeps a manifest up to date.

WORKFLOW (Dash does all of this — John touches nothing):
  1. The agent downloads a licensed model and saves the file(s) into:
         <INBOX>/<handle>/
     where <handle> is the exact handle from the manifest CSV
     (e.g. inbox/hanuman-statue/hanuman.zip).
  2. Dash runs:  python sort_stl_repository.py
  3. This script, for every <handle> folder found in the inbox:
       - looks up the product's designer from the manifest,
       - unpacks any .zip,
       - de-duplicates by content hash,
       - moves the files into  <REPO>/<designer>/<handle>/,
       - marks that row status=done in the manifest with the date + file count,
       - empties the inbox folder.
  4. Re-runnable any time. Idempotent. Works with no internet.

Status check:  python sort_stl_repository.py --status
"""

from __future__ import annotations
import csv, hashlib, shutil, sys, zipfile
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG  — set these three paths for the target machine, then leave them.
# ---------------------------------------------------------------------------
REPO     = Path(r"C:\BlackforgeSTL")                     # the permanent library
INBOX    = Path(r"C:\BlackforgeSTL\_inbox")              # where downloads land
MANIFEST = Path(r"C:\BlackforgeSTL\design_library_manifest.csv")
# Optional second copy for resilience (external drive / NAS). "" to disable.
BACKUP   = Path(r"")                                     # e.g. r"E:\BlackforgeSTL"

KEEP_EXT = {".stl", ".3mf", ".step", ".stp", ".obj", ".gcode",
            ".txt", ".pdf", ".md", ".png", ".jpg", ".jpeg"}
# ---------------------------------------------------------------------------


def safe(name: str) -> str:
    """Make a string safe for use as a folder name on Windows/macOS/Linux."""
    bad = '<>:"/\\|?*{}'
    out = "".join("_" if c in bad else c for c in name).strip().rstrip(".")
    return out or "unknown"


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> tuple[list[dict], list[str]]:
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), r.fieldnames or []


def write_manifest(rows: list[dict], fields: list[str]) -> None:
    tmp = MANIFEST.with_suffix(".tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(MANIFEST)


def status_report(rows: list[dict]) -> None:
    done = sum(1 for r in rows if r.get("status") == "done")
    total = len(rows)
    pending = total - done
    print(f"\nBlackforge STL library — {done}/{total} downloaded, {pending} pending\n")
    if pending:
        print("Next up (pending):")
        for r in [r for r in rows if r.get("status") != "done"][:10]:
            print(f"  [ ] {r['title']}  ({r['designer']})   handle: {r['handle']}")
        if pending > 10:
            print(f"  ... and {pending - 10} more")
    print()


def gather_files(folder: Path) -> list[Path]:
    """Unpack any zips in-place, then return all keepable files under folder."""
    for z in list(folder.rglob("*.zip")):
        try:
            with zipfile.ZipFile(z) as zf:
                zf.extractall(z.parent / (z.stem + "_unzipped"))
            z.unlink()
        except zipfile.BadZipFile:
            print(f"    ! bad zip skipped: {z.name}")
    return [p for p in folder.rglob("*")
            if p.is_file() and p.suffix.lower() in KEEP_EXT]


def process() -> None:
    if not MANIFEST.exists():
        sys.exit(f"Manifest not found: {MANIFEST}")
    INBOX.mkdir(parents=True, exist_ok=True)
    rows, fields = load_manifest()
    by_handle = {r["handle"]: r for r in rows}

    inbox_dirs = [d for d in INBOX.iterdir() if d.is_dir() and not d.name.startswith("_")]
    if not inbox_dirs:
        print("Inbox empty — nothing to file.")
        status_report(rows)
        return

    for d in inbox_dirs:
        handle = d.name.strip()
        row = by_handle.get(handle)
        if not row:
            print(f"  ? '{handle}' is not a known handle — left in inbox for review.")
            continue

        designer = safe(row["designer"])
        dest = REPO / designer / handle
        dest.mkdir(parents=True, exist_ok=True)

        files = gather_files(d)
        if not files:
            print(f"  - {handle}: no usable files found, skipping.")
            continue

        seen: dict[str, Path] = {}
        kept = 0
        for src in files:
            digest = sha1(src)
            if digest in seen:
                continue  # duplicate content
            seen[digest] = src
            target = dest / src.name
            n = 1
            while target.exists() and sha1(target) != digest:
                target = dest / f"{src.stem}_{n}{src.suffix}"
                n += 1
            if not target.exists():
                shutil.copy2(src, target)
                kept += 1

        # optional backup copy
        if str(BACKUP):
            bdest = BACKUP / designer / handle
            bdest.mkdir(parents=True, exist_ok=True)
            for p in dest.iterdir():
                bt = bdest / p.name
                if not bt.exists():
                    shutil.copy2(p, bt)

        row["status"] = "done"
        row["date_downloaded"] = date.today().isoformat()
        row["local_path"] = str(dest)
        row["file_count"] = str(len(list(dest.iterdir())))
        shutil.rmtree(d, ignore_errors=True)
        print(f"  + {handle}: {kept} file(s) -> {designer}\\{handle}")

    write_manifest(rows, fields)
    status_report(rows)


if __name__ == "__main__":
    if "--status" in sys.argv:
        rows, _ = load_manifest()
        status_report(rows)
    else:
        process()
