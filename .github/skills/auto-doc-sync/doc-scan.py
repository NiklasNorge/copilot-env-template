#!/usr/bin/env python3
"""Detect light-weight documentation drift between Python code and Markdown docs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List


def extract_function_signatures(py_file: Path) -> Dict[str, str]:
    signatures = {}
    content = py_file.read_text(encoding="utf-8")
    pattern = r"def\s+(\w+)\s*\((.*?)\)\s*(?:->\s*([^:]+))?:"
    for match in re.finditer(pattern, content, re.MULTILINE):
        func_name = match.group(1)
        params = match.group(2)
        return_type = match.group(3) or "None"
        signatures[func_name] = f"def {func_name}({params}) -> {return_type}"
    return signatures


def extract_docstrings(py_file: Path) -> Dict[str, str]:
    docstrings = {}
    content = py_file.read_text(encoding="utf-8")
    pattern = r'def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*[^:]+)?:\s*"""(.+?)"""'
    for match in re.finditer(pattern, content, re.DOTALL):
        docstrings[match.group(1)] = match.group(2).strip()
    return docstrings


def scan_directory(target_dir: Path, pattern: str) -> List[Path]:
    return list(target_dir.rglob(pattern))


def iter_markdown_files(search_roots: Iterable[Path]) -> Iterable[Path]:
    for root in search_roots:
        if root.exists():
            yield from root.rglob("*.md")


def has_markdown_reference(markdown_files: Iterable[Path], function_name: str) -> bool:
    pattern = re.compile(rf"\b{re.escape(function_name)}\s*\(")
    for path in markdown_files:
        content = path.read_text(encoding="utf-8")
        if pattern.search(content):
            return True
    return False


def check_drift(target_dir: Path, docs_root: Path | None) -> Dict[str, List[str]]:
    issues = {
        "missing_docstrings": [],
        "type_hints_missing": [],
        "undocumented_functions": [],
    }

    py_files = scan_directory(target_dir, "*.py")
    markdown_files = list(iter_markdown_files([docs_root] if docs_root else []))

    for py_file in py_files:
        signatures = extract_function_signatures(py_file)
        docstrings = extract_docstrings(py_file)
        for func_name, signature in signatures.items():
            if func_name.startswith("_"):
                continue
            if func_name not in docstrings:
                issues["missing_docstrings"].append(f"{py_file}: {func_name}()")
            if "-> None" in signature:
                issues["type_hints_missing"].append(f"{py_file}: {func_name}()")
            if docs_root and not has_markdown_reference(markdown_files, func_name):
                issues["undocumented_functions"].append(
                    f"{py_file}: {func_name}() not referenced in markdown docs"
                )

    return issues


def report_issues(issues: Dict[str, List[str]]) -> int:
    if not any(issues.values()):
        print("No documentation drift detected.")
        return 0

    print("\nDocumentation Drift Report\n")
    for category, items in issues.items():
        if items:
            print(f"## {category.replace('_', ' ').title()}")
            for item in items:
                print(f"  - {item}")
            print()
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_dir", help="Directory containing Python files to scan")
    parser.add_argument("--docs-root", help="Optional docs directory to scan for markdown references")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = Path(args.target_dir)
    docs_root = Path(args.docs_root) if args.docs_root else None

    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' not found")
        return 1

    return report_issues(check_drift(target_dir, docs_root))


if __name__ == "__main__":
    raise SystemExit(main())
