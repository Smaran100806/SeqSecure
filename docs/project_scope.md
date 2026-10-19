# SeqSecure: initial scope

## Problem
DNA sequence files are consumed by digital tools, so input validation is a useful defensive control in bioinformatics workflows. This project studies basic file validation and explainable statistical anomaly screening.

## In scope for the first milestone
- Parse FASTA and FASTQ.
- Check that at least one record exists.
- Check non-empty sequences.
- Check symbols against the standard IUPAC nucleotide alphabet.
- For FASTQ, confirm that quality information is parsed and its length agrees with the sequence length.
- Provide readable output and automated tests.

## Not in scope for the first milestone
- Claiming to detect DNA-encoded malware.
- Executing untrusted downstream software or attempting exploitation.
- Treating unusual sequence statistics as proof of malicious intent.
- A graph neural network or other ML model before a baseline and evaluation plan exist.

## Research questions to refine
1. How reliably can the validator identify the defined set of malformed input cases?
2. Which simple sequence features are useful for identifying deliberately defined statistical anomalies?
3. What false-positive rate occurs on a representative benign baseline?
4. What is the processing cost across file sizes?

## Evaluation principles
- Keep format-invalid cases separate from statistically unusual but valid sequences.
- Document provenance, license, preprocessing, and labels.
- Use a held-out evaluation set and avoid leakage between closely related sequences.
- Report limitations and do not equate anomaly scores with maliciousness.
