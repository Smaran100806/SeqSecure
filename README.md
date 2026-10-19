# SeqSecure

SeqSecure is a student-level, defensive cyberbiosecurity project for validating DNA sequence files and, in later milestones, screening for explainable statistical anomalies.

**Current milestone:** establish a reproducible Python project and implement basic FASTA/FASTQ validation.

## Scope and limitations

The initial version checks file readability, sequence records, nucleotide symbols, and basic FASTQ consistency. It does **not** detect malware, establish malicious intent, or prove that a file is safe. Statistical anomaly screening and evaluation will be added only after the validator and dataset plan are established.

## Requirements

- Python 3.10 or newer
- Git
- Internet access for installing dependencies

## Setup

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd SeqSecure
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- Windows Command Prompt: `.venv\\Scripts\\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Then run:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

## Run the validator

```bash
seqsecure --format fasta examples/sample.fasta
seqsecure --format fastq examples/sample.fastq
```

Exit code `0` means the file passed these basic checks. Exit code `1` means validation failed. A pass is not a security guarantee.

## Repository structure

```text
SeqSecure/
├── README.md
├── pyproject.toml
├── .gitignore
├── src/seqsecure/
│   ├── __init__.py
│   └── validator.py
├── tests/
│   └── test_validator.py
├── examples/
│   ├── sample.fasta
│   └── sample.fastq
└── docs/
    └── project_scope.md
```

## Planned milestones

1. Basic FASTA/FASTQ validation and automated tests.
2. Dataset plan: benign sequence records, malformed-format test cases, and safely generated statistical anomalies, with clear labels and provenance.
3. Explainable feature extraction: length, GC fraction, entropy, repetition/k-mer summaries, and FASTQ quality summaries.
4. Establish a rule/statistical baseline before considering an optional ML model.
5. Evaluate false positives, detection performance on defined test cases, runtime, and limitations.

## Data handling

Use only data you are permitted to access and redistribute. Record source, license, and preprocessing for every external dataset. Do not commit sensitive or restricted biological data to GitHub. Small, non-sensitive test fixtures may be committed.
