from pathlib import Path

from seqsecure.validator import validate_sequence_file


def test_valid_fasta(tmp_path: Path):
    path = tmp_path / "valid.fasta"
    path.write_text(">seq1\nACGTN\n>seq2\nGATTACA\n", encoding="utf-8")
    result = validate_sequence_file(path, "fasta")
    assert result.valid
    assert result.record_count == 2
    assert result.errors == []


def test_fasta_with_invalid_symbol_fails(tmp_path: Path):
    path = tmp_path / "invalid.fasta"
    path.write_text(">seq1\nACGTXYZ\n", encoding="utf-8")
    result = validate_sequence_file(path, "fasta")
    assert not result.valid
    assert any("non-IUPAC DNA symbol" in error for error in result.errors)


def test_empty_fasta_fails(tmp_path: Path):
    path = tmp_path / "empty.fasta"
    path.write_text("", encoding="utf-8")
    result = validate_sequence_file(path, "fasta")
    assert not result.valid
    assert result.record_count == 0


def test_valid_fastq(tmp_path: Path):
    path = tmp_path / "valid.fastq"
    path.write_text(
        "@seq1\nACGT\n+\nIIII\n"
        "@seq2\nGATTACA\n+\nIIIIIII\n",
        encoding="utf-8",
    )
    result = validate_sequence_file(path, "fastq")
    assert result.valid
    assert result.record_count == 2


def test_missing_file_fails(tmp_path: Path):
    result = validate_sequence_file(tmp_path / "missing.fasta", "fasta")
    assert not result.valid
    assert any("does not exist" in error for error in result.errors)


def test_unsupported_format_fails(tmp_path: Path):
    result = validate_sequence_file(tmp_path / "file.txt", "genbank")
    assert not result.valid
    assert any("Unsupported format" in error for error in result.errors)
