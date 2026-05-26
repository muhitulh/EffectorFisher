## Description:
This Nextflow pipeline uses Metaeuk to predict genes across populations based on a reference pan-gene set. Thereafter, it extracts isoforms and produces two key outputs: (i) Isolate-specific locus level Presence-Absence Variation (PAV) summary table and (ii) Isoform level PAV summary table. These output files serve as results and either of these outputs can also be used as inputs for Effectorfisher-core analysis for effector prediction.

## Prerequisites:
```
nextflowVersion = '>=22.03' 
singularityVersion '>=3.9.7'
```
## Required Files: 
 - **Pan-gene FASTA file:**  
   `00_pan-gene` directory

- **Assembly files Location:**
  `01_assemblies` directory; File naming convention: `{ID}.fasta`, where `{ID}` is a unique identifier for each assembly

```
Example:
EffectorFisher/
├── 00_pan-gene/
│   └── pangenes.fasta
└── 01_assemblies/
    ├── FG7.fasta
    ├── FG8.fasta
    └── sample3.fasta
```

## Installation

Install my-project in bash

```bash
  git clone https://github.com/muhitulh/EffectorFisher.git 
  cd EffectorFisher
```
    

## Run:
Execute the pipeline using one of the following commands:
```bash
bash run_local.sh
# or
sbatch run_effectorfisher.sbatch
```

## Final Results:
After running the pipeline, you will find the results organized in the `02_output` directory as follows:

### Intermediate Results:
- **Metaeuk_results:** Contains the outputs from the Metaeuk runs.
- **ignored_files.txt:** A text file listing the names of isolates for which the Metaeuk prediction did not work.

### Final Results:
- **Final_PAV_result:** Contains the final outputs of the analysis:
  - `Effector_isoform_PAV_output.txt`: Isolate-specific isoform-level PAV summary.
  - `Effector_locus_PAV_output.txt`: Isolate-specific locus-level PAV summary.
  - `iso-seq.txt`: A list of isoforms sequence with updated names.

