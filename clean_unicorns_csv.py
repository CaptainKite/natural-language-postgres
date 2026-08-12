#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


EXPECTED_HEADER = [
    "Company",
    "Valuation ($B)",
    "Date Joined",
    "Country",
    "City",
    "Industry",
    "Select Investors",
]


def normalize_cell(value: str) -> str:
    return value.strip()


def find_header_row(rows: list[list[str]]) -> tuple[int, dict[str, int]]:
    required = {name.lower() for name in EXPECTED_HEADER}

    for row_index, row in enumerate(rows):
        normalized = {
            normalize_cell(cell).lower(): column_index
            for column_index, cell in enumerate(row)
        }
        if required.issubset(normalized.keys()):
            return row_index, normalized

    raise ValueError("Could not find the unicorn data header row")


def extract_rows(rows: list[list[str]]) -> Iterable[list[str]]:
    header_index, header_map = find_header_row(rows)

    for row in rows[header_index + 1 :]:
        if not any(cell.strip() for cell in row):
            continue

        extracted = []
        for column_name in EXPECTED_HEADER:
            column_index = header_map[column_name.lower()]
            extracted.append(row[column_index].strip() if column_index < len(row) else "")

        if extracted[0]:
            yield extracted


def clean_csv(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        rows = list(reader)

    cleaned_rows = list(extract_rows(rows))

    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(EXPECTED_HEADER)
        writer.writerows(cleaned_rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean the malformed unicorn CSV exported from Excel.",
    )
    parser.add_argument("input", type=Path, help="Path to the malformed CSV file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Path for the cleaned CSV file. Defaults to <input>.cleaned.csv",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path: Path = args.input
    output_path: Path = args.output or input_path.with_name(f"{input_path.stem}.cleaned.csv")

    clean_csv(input_path, output_path)
    print(f"Wrote cleaned CSV to {output_path}")


if __name__ == "__main__":
    main()