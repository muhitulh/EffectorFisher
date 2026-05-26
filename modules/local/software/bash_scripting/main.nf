process PROCESS_FILES {
    
    input:
    tuple val(assembly), path(assembly_headers_file)

    output:
    path("${assembly}_short_summary.txt"), emit: shortSummary
    
    script:
    """
    # Generate short summary table with headers and counts in one loop
    echo -n "Assembly" > ${assembly}_short_summary.txt
    echo -n "${assembly}" > ${assembly}_short_summary_tmp.txt

    while IFS= read -r effector; do
        echo -n -e "\t\$effector" >> ${assembly}_short_summary.txt
        count=\$(grep -c "\$effector" ${assembly_headers_file})
        echo -n -e "\t\$count" >> ${assembly}_short_summary_tmp.txt
    done < ${list_file}
    echo "" >> ${assembly}_short_summary.txt
    cat ${assembly}_short_summary_tmp.txt >> ${assembly}_short_summary.txt
    echo "" >> ${assembly}_short_summary.txt  # Add a newline at the end
    rm ${assembly}_short_summary_tmp.txt
    """
}
