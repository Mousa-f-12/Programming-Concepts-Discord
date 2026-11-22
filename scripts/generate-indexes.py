#!/usr/bin/env python3
"""
Software Engineering Second Brain Index Generator
=================================================
Parses YAML frontmatter across all atomic concept records and safely
synchronizes Domain READMEs and Master Catalog indexes using delimited blocks.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_DOMAINS = [
    "fundamentals", "paradigms", "oop", "memory", "data-structures",
    "algorithms", "concurrency", "async", "databases", "networking",
    "operating-systems", "architecture", "design-patterns", "security"
]

MASTER_INVENTORY_START = "<!-- BEGIN MASTER INVENTORY -->"
MASTER_INVENTORY_END = "<!-- END MASTER INVENTORY -->"

DOMAIN_INVENTORY_START = "<!-- BEGIN DOMAIN INVENTORY -->"
DOMAIN_INVENTORY_END = "<!-- END DOMAIN INVENTORY -->"


def parse_concept_records():
    """Scan and parse all concept records in canonical domain directories."""
    records = []
    for domain in CANONICAL_DOMAINS:
        domain_dir = REPO_ROOT / domain
        if not domain_dir.exists():
            continue

        for md_path in domain_dir.glob("**/*.md"):
            if md_path.name == "README.md":
                continue

            content = md_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                continue

            try:
                metadata = yaml.safe_load(parts[1])
            except Exception as e:
                print(f"[WARN] Failed to parse frontmatter in {md_path}: {e}")
                continue

            if not isinstance(metadata, dict):
                continue

            rel_path = md_path.relative_to(REPO_ROOT).as_posix()
            records.append({
                "path": rel_path,
                "abs_path": md_path,
                "domain": metadata.get("domain", domain),
                "category": metadata.get("category", "general"),
                "subcategory": metadata.get("subcategory", "general"),
                "id": metadata.get("id", ""),
                "title": metadata.get("title", md_path.stem),
                "type": metadata.get("type", "concept"),
                "status": metadata.get("status", "draft"),
                "tags": metadata.get("tags", []),
                "prerequisites": metadata.get("prerequisites", []),
                "related": metadata.get("related", [])
            })

    return records


def build_master_inventory_markdown(records):
    """Build Markdown table for the Master README."""
    if not records:
        return "_No active concept records found._\n"

    lines = [
        "| Domain | Category | Subcategory | Concept Title / Record | Type | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    # Sort records by domain, category, subcategory, title
    sorted_records = sorted(
        records,
        key=lambda r: (r["domain"], r["category"], r["subcategory"], r["title"])
    )

    for r in sorted_records:
        domain_link = f"[`{r['domain']}`]({r['domain']}/README.md)"
        record_link = f"[{r['title']}]({r['path']})"
        lines.append(
            f"| {domain_link} | `{r['category']}` | `{r['subcategory']}` | {record_link} | `{r['type']}` | `{r['status']}` |"
        )

    lines.append("")
    return "\n".join(lines)


def build_domain_inventory_markdown(domain_records, domain_name):
    """Build Category/Subcategory Markdown tables for a Domain README."""
    if not domain_records:
        return "_No active concept records currently provisioned for this domain._\n"

    # Group by category -> subcategory
    hierarchy = defaultdict(lambda: defaultdict(list))
    for r in domain_records:
        hierarchy[r["category"]][r["subcategory"]].append(r)

    lines = []
    for category, subcategories in sorted(hierarchy.items()):
        lines.append(f"### Category: `{category}`")
        lines.append("")
        for subcategory, recs in sorted(subcategories.items()):
            lines.append(f"#### Subcategory: `{subcategory}`")
            lines.append("")
            lines.append("| Concept ID | Title / Record | Type | Status |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for r in recs:
                # Relative to domain dir
                rel_to_domain = Path(r["path"]).relative_to(domain_name).as_posix()
                link = f"[{r['title']}]({rel_to_domain})"
                lines.append(f"| `{r['id']}` | {link} | `{r['type']}` | `{r['status']}` |")
            lines.append("")

    return "\n".join(lines)


def update_delimited_content(filepath: Path, start_marker: str, end_marker: str, new_content: str, check_only: bool = False):
    """Safely replace content between start_marker and end_marker."""
    if not filepath.exists():
        print(f"[WARN] Target file does not exist: {filepath}")
        return False

    original_text = filepath.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        flags=re.DOTALL
    )

    replacement = f"{start_marker}\n\n{new_content}\n{end_marker}"

    if pattern.search(original_text):
        updated_text = pattern.sub(replacement, original_text)
    else:
        # Markers not present; append or insert under appropriate section
        print(f"[INFO] Delimiters not found in {filepath.name}; adding them.")
        updated_text = original_text.rstrip() + f"\n\n{start_marker}\n\n{new_content}\n{end_marker}\n"

    if updated_text == original_text:
        return True

    if check_only:
        print(f"[OUT-OF-SYNC] {filepath.name} index requires updating.")
        return False

    filepath.write_text(updated_text, encoding="utf-8")
    print(f"[UPDATED] Synchronized index in {filepath.name}.")
    return True


def main():
    check_mode = "--check" in sys.argv
    records = parse_concept_records()
    print(f"Loaded {len(records)} active concept record(s) across canonical domains.")

    all_in_sync = True

    # 1. Update Master README
    master_readme = REPO_ROOT / "README.md"
    master_content = build_master_inventory_markdown(records)
    if not update_delimited_content(
        master_readme,
        MASTER_INVENTORY_START,
        MASTER_INVENTORY_END,
        master_content,
        check_only=check_mode
    ):
        all_in_sync = False

    # 2. Update Domain READMEs
    domain_groups = defaultdict(list)
    for r in records:
        domain_groups[r["domain"]].append(r)

    for domain_name, dom_records in domain_groups.items():
        dom_readme = REPO_ROOT / domain_name / "README.md"
        dom_content = build_domain_inventory_markdown(dom_records, domain_name)
        if not update_delimited_content(
            dom_readme,
            DOMAIN_INVENTORY_START,
            DOMAIN_INVENTORY_END,
            dom_content,
            check_only=check_mode
        ):
            all_in_sync = False

    if check_mode:
        if all_in_sync:
            print("SUCCESS: All indexes are in sync.")
            sys.exit(0)
        else:
            print("FAILED: One or more indexes are out of sync. Run python3 scripts/generate-indexes.py to update.")
            sys.exit(1)
    else:
        print("SUCCESS: All domain and master indexes synchronized successfully.")


if __name__ == "__main__":
    main()
