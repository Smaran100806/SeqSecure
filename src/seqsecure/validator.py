"""Basic defensive validation for FASTA and FASTQ DNA sequence files.

This module validates file structure and DNA alphabet conventions. It does not
detect malware and a successful result is not a guarantee that a file is safe.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from Bio import SeqIO
from Bio.SeqIO import InsdcIO

# Standard IUPAC nucleotide symbols, including ambiguity codes.
DNA_IUPAC = set("ACGTRYSWKMBDHVN")


@dataclass
class ValidationResult:
    path: str
    file_format: str
    valid: bool
    record_count: int
    errors: list[str]

    def summary(self) -> str:
        status = "PASS" if self.valid else "FAIL"
        lines = [
            f"{status}: {self.path}",
            f"Format: {self.file_format.upper()}",
            f"Records parsed: {self.record_count}",
        ]
        if self.errors:
            lines.append("Issues:")
            lines.extend(f"- {error}" for error in self.errors)
        else:
            lines.append(
                "Basic format and DNA-symbol checks passed; this is not a security guarantee."
            )
        return "\n".join(lines)


def validate_sequence_file(path: str | Path, file_format: str) -> ValidationResult:
    """Validate basic FASTA or FASTQ structure and nucleotide symbols."""
    file_path = Path(path)
    fmt = file_format.lower().strip()
    errors: list[str] = []
    record_count = 0

    if fmt not in {"fasta", "fastq"}:
        return ValidationResult(str(file_path), fmt, False, 0,
                                ["Unsupported format. Choose 'fasta' or 'fastq'."])

    if not file_path.exists():
        return ValidationResult(str(file_path), fmt, False, 0, ["File does not exist."])
    if not file_path.is_file():
        return ValidationResult(str(file_path), fmt, False, 0, ["Path is not a regular file."])

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            for record_index, record in enumerate(SeqIO.parse(handle, fmt), start=1):
                record_count += 1
                sequence = str(record.seq)
                if not sequence:
                    errors.append(f"Record {record_index} has an empty sequence.")

                invalid_symbols = sorted(set(sequence.upper()) - DNA_IUPAC)
                if invalid_symbols:
                    symbols = ", ".join(repr(symbol) for symbol in invalid_symbols)
                    errors.append(
                        f"Record {record_index} contains non-IUPAC DNA symbol(s): {symbols}."
                    )

                if fmt == "fastq":
                    qualities = record.letter_annotations.get("phred_quality")
                    if qualities is None:
                        errors.append(
                            f"Record {record_index} has no parsed FASTQ quality scores."
                        )
                    elif len(qualities) != len(sequence):
                        errors.append(
                            f"Record {record_index} has sequence/quality length mismatch."
                        )

    except Exception as exc:
        # Biopython parser exceptions vary by format/version. Report the failure
        # instead of exposing a traceback to a normal CLI user.
        errors.append(f"Could not parse file: {type(exc).__name__}: {exc}")

    if record_count == 0 and not errors:
        errors.append("No sequence records were found.")

    return ValidationResult(
        path=str(file_path),
        file_format=fmt,
        valid=(record_count > 0 and not errors),
        record_count=record_count,
        errors=errors,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Perform basic defensive validation of a FASTA or FASTQ file."
    )
    parser.add_argument("--format", required=True, choices=["fasta", "fastq"],
                        help="Input file format.")
    parser.add_argument("path", help="Path to the sequence file.")
    args = parser.parse_args(argv)

    result = validate_sequence_file(args.path, args.format)
    print(result.summary())
    return 0 if result.valid else 1


if __name__ == "__main__":
    sys.exit(main())
