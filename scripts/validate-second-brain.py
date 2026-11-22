#!/usr/bin/env python3
"""
Software Engineering Second Brain Validator (Hardened Edition)
==============================================================
Validates repository architecture, strict taxonomy, kebab-case naming,
YAML frontmatter metadata, link integrity, and content preservation.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent

# 14 Canonical domains specified in taxonomy
CANONICAL_DOMAINS = {
    "fundamentals", "paradigms", "oop", "memory", "data-structures",
    "algorithms", "concurrency", "async", "databases", "networking",
    "operating-systems", "architecture", "design-patterns", "security"
}

NON_DOMAIN_DIRS = {"scripts", "docs", ".git", ".github"}

REQUIRED_FRONTMATTER_FIELDS = ["id", "domain", "prerequisites", "related"]

# Kebab-case patterns
KEBAB_DIR_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KEBAB_FILE_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)+$")

# Link extraction regex handling optional titles and angle brackets
MARKDOWN_LINK_REGEX = re.compile(r"\[([^\]]+)\]\((?:<([^>]+)>|([^\s\)\"]+))(?:\s+\"[^\"]*\")?\)")

# Pre-migration content preservation test markers
PRESERVATION_REGISTRY = {
    "databases/relational-databases/t-sql/temporary-tables-vs-table-variables.md": [
        "الفرق بين Temporary Tables و Table Variables في T-SQL",
        "Definition and Scope — التعريف والنطاق",
        "Lifetime — دورة الحياة",
        "Performance and Usage — الأداء والاستخدام",
        "Transaction Logs — سجلات المعاملات",
        "Use Cases — حالات الاستخدام",
        "خلاصة المقارنة",
        "ملاحظة هندسية",
        "#Temp",
        "@Temp",
        "tempdb",
        "ROLLBACK"
    ]
}


def strip_code_blocks(markdown_text: str) -> str:
    """Strip fenced code blocks and inline code to prevent false-positive link matches."""
    # Strip multi-line code fences (``` or ~~~)
    stripped = re.sub(r"(```|~~~).*?\1", "", markdown_text, flags=re.DOTALL)
    # Strip inline code spans
    stripped = re.sub(r"`[^`\n]+`", "", stripped)
    return stripped


def check_naming_conventions():
    errors = []
    print("[-] Checking naming conventions (kebab-case)...")

    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip git directory
        if ".git" in root.split(os.sep):
            continue

        rel_root = Path(root).relative_to(REPO_ROOT)
        rel_root_parts = rel_root.parts

        # Check directories
        for d in dirs:
            if d.startswith("."):
                continue
            if not KEBAB_DIR_PATTERN.match(d):
                errors.append(f"Directory name not kebab-case: '{rel_root / d}'")

        # Check files
        for f in files:
            if f.startswith("."):
                continue
            if f == "README.md":
                continue
            if not KEBAB_FILE_PATTERN.match(f):
                errors.append(f"File name not kebab-case: '{rel_root / f}'")

    if not errors:
        print("    [PASS] All tracked files and directories conform to kebab-case.")
    else:
        for err in errors:
            print(f"    [FAIL] {err}")
    return errors


def check_taxonomy_and_frontmatter():
    errors = []
    print("[-] Checking hierarchy depth and YAML frontmatter...")

    # Collect all concept records inside canonical domain folders
    concept_records = []
    registered_ids = {}

    for domain in CANONICAL_DOMAINS:
        domain_dir = REPO_ROOT / domain
        if not domain_dir.exists():
            continue

        for p in domain_dir.glob("**/*.md"):
            if p.name == "README.md":
                continue
            concept_records.append(p)

    print(f"    Found {len(concept_records)} active atomic concept record(s) in canonical domains.")

    for md_path in concept_records:
        rel_path = md_path.relative_to(REPO_ROOT)
        parts = rel_path.parts

        # Expecting: <domain>/<category>/<subcategory>/<concept>.md (4 tiers)
        if len(parts) != 4:
            errors.append(
                f"File '{rel_path}' does not adhere to strict 4-tier taxonomy "
                f"(Domain > Category > Subcategory > Concept Record). Found {len(parts)} tiers."
            )
            continue

        domain, category, subcategory, filename = parts
        if domain not in CANONICAL_DOMAINS:
            errors.append(f"Domain '{domain}' in '{rel_path}' is not a canonical domain.")

        # Read file and parse YAML frontmatter
        content = md_path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            errors.append(f"File '{rel_path}' is missing YAML frontmatter header ('---').")
            continue

        parts_content = content.split("---", 2)
        if len(parts_content) < 3:
            errors.append(f"File '{rel_path}' has malformed frontmatter delimiter.")
            continue

        frontmatter_raw = parts_content[1]
        try:
            metadata = yaml.safe_load(frontmatter_raw)
        except Exception as e:
            errors.append(f"File '{rel_path}' has invalid YAML frontmatter: {e}")
            continue

        if not isinstance(metadata, dict):
            errors.append(f"File '{rel_path}' frontmatter did not parse into a dictionary.")
            continue

        # Check required fields
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in metadata or metadata[field] is None:
                errors.append(f"File '{rel_path}' frontmatter missing required field: '{field}'")

        # Check ID uniqueness and format
        cid = metadata.get("id")
        if cid:
            if cid in registered_ids:
                errors.append(f"Duplicate Concept ID '{cid}' in '{rel_path}' (already defined in '{registered_ids[cid]}').")
            else:
                registered_ids[cid] = rel_path

        # Validate domain, category, subcategory alignment
        if metadata.get("domain") != domain:
            errors.append(
                f"File '{rel_path}' frontmatter domain '{metadata.get('domain')}' "
                f"does not match directory domain '{domain}'"
            )

        if metadata.get("category") != category:
            errors.append(
                f"File '{rel_path}' frontmatter category '{metadata.get('category')}' "
                f"does not match directory category '{category}'"
            )

        if metadata.get("subcategory") != subcategory:
            errors.append(
                f"File '{rel_path}' frontmatter subcategory '{metadata.get('subcategory')}' "
                f"does not match directory subcategory '{subcategory}'"
            )

    if not errors:
        print(f"    [PASS] Validated {len(concept_records)} concept record(s) with valid 4-tier taxonomy and frontmatter.")
    else:
        for err in errors:
            print(f"    [FAIL] {err}")
    return errors, registered_ids


def check_metadata_graph_and_links(registered_ids):
    errors = []
    print("[-] Checking internal Markdown links and semantic graph references...")

    all_md_files = [p for p in REPO_ROOT.glob("**/*.md") if ".git" not in p.parts]
    link_count = 0

    existing_paths = {p.relative_to(REPO_ROOT).as_posix() for p in all_md_files}
    concept_paths_without_ext = {
        (p.relative_to(REPO_ROOT).with_suffix("")).as_posix() for p in all_md_files
    }

    # 1. Check physical markdown links
    for md_path in all_md_files:
        rel_path = md_path.relative_to(REPO_ROOT)
        content = md_path.read_text(encoding="utf-8")

        # Strip code blocks to avoid false positives
        clean_content = strip_code_blocks(content)

        for match in MARKDOWN_LINK_REGEX.finditer(clean_content):
            link_text = match.group(1)
            target = match.group(2) or match.group(3)
            if not target:
                continue

            target = target.strip()
            # Skip external or anchor-only links
            if target.startswith(("http://", "https://", "mailto:", "ftp:")):
                continue
            if target.startswith("#"):
                continue

            # Strip query or anchor fragment
            target_clean = target.split("#")[0].split("?")[0]
            if not target_clean:
                continue

            link_count += 1
            resolved = (md_path.parent / target_clean).resolve()

            if not resolved.exists():
                errors.append(
                    f"Broken link in '{rel_path}': [{link_text}]({target}) -> Target '{resolved}' not found."
                )

    # 2. Check semantic graph references (prerequisites & related)
    existing_refs = 0
    planned_refs = 0

    for domain in CANONICAL_DOMAINS:
        domain_dir = REPO_ROOT / domain
        if not domain_dir.exists():
            continue

        for p in domain_dir.glob("**/*.md"):
            if p.name == "README.md":
                continue

            content = p.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue

            parts_content = content.split("---", 2)
            if len(parts_content) < 3:
                continue

            try:
                metadata = yaml.safe_load(parts_content[1])
            except Exception:
                continue

            for field in ["prerequisites", "related"]:
                refs = metadata.get(field, [])
                if isinstance(refs, list):
                    for ref in refs:
                        ref_str = str(ref).strip()
                        # Check if ref corresponds to an existing file or ID
                        if (
                            ref_str in registered_ids
                            or ref_str in existing_paths
                            or ref_str in concept_paths_without_ext
                        ):
                            existing_refs += 1
                        else:
                            # It's a declared planned concept
                            planned_refs += 1

    print(f"    [INFO] Verified {link_count} physical markdown links.")
    print(f"    [INFO] Semantic Knowledge Graph: {existing_refs} live reference(s), {planned_refs} planned conceptual reference(s).")

    if not errors:
        print("    [PASS] All internal Markdown links resolved successfully.")
    else:
        for err in errors:
            print(f"    [FAIL] {err}")
    return errors


def check_content_preservation():
    errors = []
    print("[-] Checking content preservation against historical records...")

    for rel_file, markers in PRESERVATION_REGISTRY.items():
        target_path = REPO_ROOT / rel_file
        if not target_path.exists():
            errors.append(f"Preserved record missing from repository: '{rel_file}'")
            continue

        content = target_path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                errors.append(f"Content preservation marker missing in '{rel_file}': '{marker}'")

    if not errors:
        print(f"    [PASS] All {sum(len(m) for m in PRESERVATION_REGISTRY.values())} preservation markers successfully verified.")
    else:
        for err in errors:
            print(f"    [FAIL] {err}")
    return errors


def main():
    print("=" * 65)
    print("Software Engineering Second Brain Quality Assurance Suite")
    print("=" * 65)

    all_errors = []
    all_errors.extend(check_naming_conventions())
    taxonomy_errors, registered_ids = check_taxonomy_and_frontmatter()
    all_errors.extend(taxonomy_errors)
    all_errors.extend(check_metadata_graph_and_links(registered_ids))
    all_errors.extend(check_content_preservation())

    print("=" * 65)
    if not all_errors:
        print("SUCCESS: All Knowledge Architecture validation checks PASSED cleanly!")
        sys.exit(0)
    else:
        print(f"FAILED: Found {len(all_errors)} validation error(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
