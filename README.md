# functional-annotation-tools

Tools and scripts for functional annotation of metagenomic sequences, mapping predicted genes to functional databases such as KEGG, COG, and Pfam.

## Overview

This repository provides a lightweight command-line tool for annotating predicted genes from a metagenomic assembly against a local functional reference table (for example, gene-to-KEGG, gene-to-COG, or gene-to-Pfam mappings produced by tools like eggNOG-mapper, InterProScan, or KOfamScan).

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python scripts/annotate_genes.py --genes examples/example_genes.faa --mapping examples/example_mapping.tsv --output annotations.tsv
```

## Input format

The mapping file must be a tab-separated file with these columns: gene_id, function_id, description, database.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
