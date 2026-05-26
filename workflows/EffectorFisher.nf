
//--------------------------------------------------
// Workflow EffectorFisher
//--------------------------------------------------


include { ANNOTATE_PROTEINS }       from '../subworkflow/local/annotate_proteins/main'

// Checks for input files
//pangenes = Channel.fromPath(params.pangenes, type: 'file')


workflow EFFECTORFISHER_WORKFLOW {

    // Create a channel from the input assembly files
    Channel
        .fromPath(params.assembly_dir)
        .map { file -> tuple(file.baseName.replace("_assembly", ""), file) }
        .set { samples }

    // Annotate isoforms and process output
    ANNOTATE_PROTEINS(samples, params.pangenes)

    //Run Predector here
    // Add here subworkflow for predector
    //--------------------------------------------

    // Run EffectorFisher-core
    // Use output from ANNOTATE_PROTEINS and predector
    //--------------------------------------------
}
