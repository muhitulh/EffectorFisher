#!/usr/bin/env python3

# Author: Dr. Kristina K. Gagalova
# Date: 31 Jan 2025
# Description: process annotation output into tabular output, counting the number of variants

import os
import re
import argparse
import pandas as pd
from collections import defaultdict, Counter
from Bio import SeqIO
import sys

def clean_gene_name(raw_name):
    """
    Cleans gene names by keeping only the part before the first '|'.
    """
    return raw_name.split('|')[0]

def aggregate_gene_counts(df, output_aggregated_tsv='Effector_locus_PAV_output.txt'):
    """
    Aggregates gene counts by summing up counts for genes with _1, _2 suffixes.
    Includes file name for output reference.
    """
    base_gene_names = {}
    for col in df.columns[1:]:  # Skip ID column
        base_name = col.rsplit('_', 1)[0]  # Remove _1, _2, etc.
        if base_name not in base_gene_names:
            base_gene_names[base_name] = []
        base_gene_names[base_name].append(col)
    
    aggregated_df = pd.DataFrame(index=df.index)
    aggregated_df['ID'] = df['ID']
    
    for base_name, variants in base_gene_names.items():
        aggregated_df[base_name] = df[variants].sum(axis=1)
    
    aggregated_df.to_csv(output_aggregated_tsv, sep='\t', index=False)
    return aggregated_df

def process_fasta(file_paths, output_individual_tsv='Effector_locus_PAV_output.txt', output_gene_map_tsv='iso-seq.txt'):
    """
    Processes multiple FASTA files, extracts gene names, and counts occurrences across files.
    Also generates a mapping of original gene names to unique gene names.
    """
    file_genes = {}  # Stores gene counts per file
    gene_counter = defaultdict(int)  # Tracks counts for each gene name
    fasta_ext_pattern = re.compile(r'\.(fasta|fna|faa|fa|fas)$', re.IGNORECASE)
    gene_map = []  # Stores mappings of original gene names to unique names
    sequence_to_genes = defaultdict(set)  # Maps sequences to unique gene names (use set to avoid duplicates)
    sequence_to_unique_gene = {}  # Maps sequences to unique gene names

    for file_path in file_paths:
        base_name = os.path.basename(file_path)  # Extract file name
        base_name = fasta_ext_pattern.sub('', base_name)  # Remove file extension
        file_genes[base_name] = defaultdict(int)  # Initialize gene count dictionary

        for record in SeqIO.parse(file_path, 'fasta'):
            gene_name = clean_gene_name(record.id)  # Extract and clean gene name
            seq_str = str(record.seq)  # Convert sequence to string
            
            if seq_str not in sequence_to_unique_gene:
                # If sequence is new, create a unique gene name
                gene_counter[gene_name] += 1
                unique_gene_name = f"{gene_name}_{gene_counter[gene_name]}"
                sequence_to_unique_gene[seq_str] = unique_gene_name
            else:
                # Otherwise, reuse the existing unique gene name
                unique_gene_name = sequence_to_unique_gene[seq_str]
            
            if [unique_gene_name, seq_str] not in gene_map:
                gene_map.append([unique_gene_name, seq_str])
            
            file_genes[base_name][unique_gene_name] += 1  # Increment gene count
            
    all_gene_names = sorted(set().union(*file_genes.values()))  # Collect all unique gene names
    df = pd.DataFrame(index=file_genes.keys(), columns=['ID'] + all_gene_names)  # Create DataFrame
    df['ID'] = df.index  # Assign file names as IDs
    df = df.infer_objects(copy=False)
    df.fillna(0, inplace=True)  # Fill missing values with 0
    df[all_gene_names] = df[all_gene_names].astype(int)  # Ensure integer values

    for file, genes in file_genes.items():
        for gene, count in genes.items():
            df.at[file, gene] = count  # Assign counts in DataFrame

    df = df.sort_index()
    df = df[['ID'] + sorted(df.columns[1:])]  # Ensure sorted column order
    df.to_csv(output_individual_tsv, sep='\t', index=False)  # Save individual counts
    
    # Save the gene mapping table
    gene_map_df = pd.DataFrame(gene_map, columns=['isoform', 'sequence'])
    gene_map_df.to_csv(output_gene_map_tsv, sep='\t', index=False)

    return df  # Return DataFrame

def main():
    parser = argparse.ArgumentParser(
        description="Process one or more FASTA files to extract aggregated gene counts from annotations."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Comma-separated list of input FASTA file paths."
    )
    parser.add_argument(
        "-oi", "--output_individual",
        type=str,
        default="Effector_variants_PAV_output.txt",
        help="Path to save the individual counts output TSV file (default: Effector_variants_PAV_output.txt)."
    )
    parser.add_argument(
        "-oa", "--output_aggregated",
        type=str,
        default="Effector_locus_PAV_output.txt",
        help="Path to save the aggregated counts output TSV file (default: Effector_locus_PAV_output.txt)."
    )
    parser.add_argument(
        "-om", "--output_gene_map",
        type=str,
        default="iso-seq.txt",
        help="Path to save the gene mapping output TSV file (default: iso-seq.txt)."
    )
    args = parser.parse_args()

    file_paths = args.input.split(',')
    output_individual_tsv = args.output_individual
    output_aggregated_tsv = args.output_aggregated
    output_gene_map_tsv = args.output_gene_map
    
    try:
        df = process_fasta(file_paths, output_individual_tsv, output_gene_map_tsv)
        aggregated_df = aggregate_gene_counts(df, output_aggregated_tsv)
        print(f"Processed FASTA files: {', '.join(file_paths)}")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
