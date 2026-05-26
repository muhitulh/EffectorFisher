#!/bin/bash --login

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=64GB
#SBATCH --partition=work
#SBATCH --time=1-00:00:00
#SBATCH --account=y95
#SBATCH --export=NONE

#module load nextflow/22.10.0
module load nextflow/23.10.0
module load singularity/4.1.0-nompi

# IMPORTANT: singularity cache dir needs to be specified in order to download image when running pante2 default
#export NXF_SINGULARITY_CACHEDIR="./work"

nextflow run ./main.nf \
    -profile pawsey_setonix,singularity \
    -resume \
    --assembly_dir "${PWD}/01_assemblies/*.fasta" \
    --pangenes "${PWD}/00_pan-gene/pangenes.fasta" \
    --tool EffectorFisher
