#!/usr/bin/env python3
"""
annotate_genes.py

Annotate predicted genes from a metagenomic assembly against functional
databases (KEGG, COG, Pfam) using a local mapping/reference table.

Usage:
    python annotate_genes.py --genes genes.faa --mapping mapping.tsv --output annotations.tsv

The mapping file should be a tab-separated file with at least these columns:
    gene_id    function_id    description    database

Typical mapping files can be generated from tools such as eggNOG-mapper,
InterProScan, or KOfamScan output, reformatted into this simple schema.
"""

import argparse
import csv
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Annotate genes with functional categories (KEGG/COG/Pfam)."
    )
    parser.add_argument("--genes", required=True, help="FASTA file of predicted gene/protein sequences.")
    parser.add_argument("--mapping", required=True, help="TSV mapping file: gene_id, function_id, description, database.")
    parser.add_argument("--output", required=True, help="Path to write the annotation report (TSV).")
    return parser.parse_args()


def load_gene_ids(fasta_path):
    """Extract gene/protein IDs from a FASTA file's headers."""
    gene_ids = []
    with open(fasta_path) as handle:
        for line in handle:
            if line.startswith(">"):
                gene_id = line[1:].strip().split()[0]
                gene_ids.append(gene_id)
    return gene_ids


def load_mapping(mapping_path):
    """Load the gene_id -> functional annotation mapping table."""
    mapping = {}
    with open(mapping_path) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required_cols = {"gene_id", "function_id", "description", "database"}
        if not required_cols.issubset(reader.fieldnames or []):
            sys.exit(
                f"Mapping file must contain columns: {sorted(required_cols)}. "
                f"Found: {reader.fieldnames}"
            )
        for row in reader:
            mapping.setdefault(row["gene_id"], []).append(row)
    return mapping


def annotate(gene_ids, mapping):
    """Match gene IDs against the mapping table and collect annotations."""
    results = []
    annotated = 0
    for gene_id in gene_ids:
        hits = mapping.get(gene_id)
        if hits:
            annotated += 1
            results.extend(hits)
        else:
            results.append({
                "gene_id": gene_id,
                "function_id": "NA",
                "description": "no hit",
                "database": "NA",
            })
    return results, annotated


def write_report(results, output_path):
    fieldnames = ["gene_id", "function_id", "description", "database"]
    with open(output_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(results)


def main():
    args = parse_args()

    if not Path(args.genes).exists():
        sys.exit(f"Gene FASTA file not found: {args.genes}")
    if not Path(args.mapping).exists():
        sys.exit(f"Mapping file not found: {args.mapping}")

    gene_ids = load_gene_ids(args.genes)
    mapping = load_mapping(args.mapping)
    results, annotated = annotate(gene_ids, mapping)
    write_report(results, args.output)

    total = len(gene_ids)
    pct = (annotated / total * 100) if total else 0
    print(f"Annotated {annotated}/{total} genes ({pct:.1f}%). Report written to {args.output}")


if __name__ == "__main__":
    main()
