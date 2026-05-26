//
// Subworkflow - annotate variants
//

include { METAEUK_EASYPREDICT }  from '../../../modules/nf-core/metaeuk/easypredict/main'
include { PROCESS_ANNOTATIONS }  from '../../../modules/local/software/python_scripts'


workflow ANNOTATE_PROTEINS {
    
    take:
    sample_assembly    // tuple [ sample, assembly ]
    pangenes           // val(path_fasta)

    main:

    // Run Metaeuk
    metaeuk_out = METAEUK_EASYPREDICT(sample_assembly, pangenes)

    // Get output files
    metaeuk_out.faa
        .map { it -> it[1] }
        .collect()
        .set { all_metaeuk_output }
    
    // Process variants table
    table_vars = PROCESS_ANNOTATIONS(all_metaeuk_output)
    
    emit:
    metaeuk_out.faa
    table_vars.byLocIdTable
    table_vars.bySeqIdTable
    table_vars.seqIso

}

