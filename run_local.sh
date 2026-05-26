#!/usr/bin/bash

# Load required modules if the module command is available
if command -v module &> /dev/null; then
    module load nextflow/23.10.0
    module load singularity/4.1.0-nompi
fi

# Set Singularity cache directory
export NXF_SINGULARITY_CACHEDIR=./work

# Run Nextflow pipeline
nextflow run main.nf \
    -profile local,singularity \
    -resume \
    --assembly_dir "${PWD}/01_assemblies/*.fasta" \
    --pangenes "${PWD}/00_pan-gene/pangenes.fasta" \
    --tool EffectorFisher
