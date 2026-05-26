process PROCESS_ANNOTATIONS {

    label 'python_processing'

    container 'community.wave.seqera.io/library/pandas_pip_biopython:465ab8e47f7a0510'

    input:
    path(proteinFiles) // [file1, file2, file3...] list of fasta files

    output:
    path("Effector_variants_PAV_output.txt"), emit: bySeqIdTable
    path("Effector_locus_PAV_output.txt")   , emit: byLocIdTable
    path("iso-seq.txt")                     , emit: seqIso

    script:
    """
    process_table.py -i ${proteinFiles.findAll().join(',') }
    """
}
