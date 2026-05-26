#!/usr/bin/env nextflow

nextflow.enable.dsl=2

// Validation - validation from nf-core for input results
include { validateParameters; paramsHelp; paramsSummaryLog; fromSamplesheet } from 'plugin/nf-validation'

// Validate input parameters - help menu
validateParameters()

if (params.help) {
   log.info paramsHelp("nextflow run ./main.nf ...")
   exit 0
}

// Print summary of supplied parameters - no need of this
log.info paramsSummaryLog(workflow)


// This part calls the workflows
workflow_input = params.tool
switch (workflow_input) {
    case ["EffectorFisher"]:
        include { EFFECTORFISHER_WORKFLOW } from './workflows/EffectorFisher.nf'
	break;
}

// Main workflow used to select from themes and tools
workflow {
    
    if (params.tool == "EffectorFisher") {
        EFFECTORFISHER_WORKFLOW()
    } else {
        println("Please provide the correct input options")
    }		 
}
