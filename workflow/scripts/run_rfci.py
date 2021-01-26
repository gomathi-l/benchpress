import os

# This is an ugly but nice wrapper.
command = None
if snakemake.wildcards["test"] in ["bdeu-test"]:
    # Removes the data range header on the second row. 
    
    command = ("sed '2d' {dataset} > {adjmat}.no_range_header && "
                "/usr/bin/time -f \"%e\" -o {time} " 
                "java -jar workflow/scripts/tetrad/causal-cmd-1.1.3-jar-with-dependencies.jar " 
                "--algorithm rfci "
                "--data-type {datatype} "
                "--dataset {adjmat}.no_range_header "
                "--delimiter space " 
                "--test {test} "
                "--alpha {alpha} "
                "--json-graph "    
                "--prefix {adjmat} " 
                "&& rm -f {adjmat}.no_range_header "
                '&& Rscript workflow/scripts/tetrad_graph_to_adjmat.R ' 
                '--jsongraph {adjmat}_graph.json ' 
                '--filename {adjmat} ' 
                '&& ' 
                'rm {adjmat}_graph.json ' 
                '&& ' 
                'rm {adjmat}.txt').format(dataset=snakemake.input["data"], **snakemake.output, **snakemake.wildcards)

if snakemake.wildcards["test"] in ["chi-square-test", "cg-lr-test"]:

    command = ("/usr/bin/time -f \"%e\" -o {time} " 
                "java -jar workflow/scripts/tetrad/causal-cmd-1.1.3-jar-with-dependencies.jar " 
                "--algorithm rfci "
                "--data-type {datatype} "
                "--dataset {dataset} "
                "--delimiter space " 
                "--test {test} "
                "--alpha {alpha} "
                "--json-graph "    
                "--prefix {adjmat} " 
                '&& Rscript workflow/scripts/tetrad_graph_to_adjmat.R ' 
                '--jsongraph {adjmat}_graph.json ' 
                '--filename {adjmat} ' 
                '&& ' 
                'rm {adjmat}_graph.json ' 
                '&& ' 
                'rm {adjmat}.txt').format(dataset=snakemake.input["data"], **snakemake.output, **snakemake.wildcards)

os.system(command)