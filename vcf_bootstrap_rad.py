#!/usr/bin/env python

import argparse
import pandas as pd
from io import StringIO
from concurrent.futures import ProcessPoolExecutor

### Parse arguments
def get_args():
    psr = argparse.ArgumentParser(
        usage = "vcf_bootstrap.py [OPTIONS]",
        description = (
            "This script performs bootstrapping for a VCF file.\
            If being under blocked-boostrapping (--blocked_bootstrap), SNPs are divided into each locus and sampling loci with replacement.\
            In this case, the CHROM column must has the locus name."
        )
    )
    psr.add_argument(
        "-i", "--input",
        help = "Input file in vcf format",
        required = True,
        type = str
    )
    psr.add_argument(
        "-n", "--number_of_bootstrap",
        help = "Number of bootstrapping",
        required = True,
        type = int
    )
    psr.add_argument(
        "--blocked_bootstrap",
        help = "Force to do BLOCKED bootstrapping.\
        The SNPs are chunked based on the CHROM column, \
        and sampling from the chunks. This is suitable for ipyrad outputs,\
        but not for other formats. The CHROM column must has unique locus name",
        action="store_true"
    )

    args = psr.parse_args()
    return args


if __name__ == "__main__": 
    ### Get arguments
    args = get_args()
    input_vcf              = args.input
    n_boot                 = args.number_of_bootstrap
    does_blocked_bootstrap = args.blocked_bootstrap

    
    ### Open the input file and get the header content
    with open(input_vcf, "r") as infile:
        lines = infile.readlines()
    header_lines = [line for line in lines if line.startswith("#")]
    snps_lines = [line for line in lines if not line.startswith("#")]
    header_content = "".join(header_lines)


    ### Load the SNPs data
    snps_data = StringIO("".join(snps_lines))
    snps_df = pd.read_table(snps_data, header=None, sep="\t")
    snps_df = snps_df.rename(columns={0: "CHROM", 1: "POS", 2: "ID", 3: "REF", 4: "ALT", 5:"QUAL", 6: "FILTER", 7: "INFO", 8: "FORMAT"})


    for boot_id in range(1, n_boot+1):
        ### Perform bootstrap sampling under multiprocessing
        ### Blocked-boostraping
        if does_blocked_bootstrap == True:   
            chunks = [chunk for _, chunk in snps_df.groupby("CHROM")]
            sampled_chunks = [chunks[i] for i in pd.Series(range(len(chunks))).sample(len(chunks), replace = True).sort_values()]
            
            ### Label "CHROM" column with unique numbers for each sampled chunk
            sampled_df = pd.concat(
                sampled_chunks, 
                ignore_index=True
            ).assign(CHROM=lambda df: pd.Series(range(1, len(sampled_chunks) + 1)).repeat([len(chunk) for chunk in sampled_chunks]).values)

        ### Normal bootstrapping
        else:
            sampled_df = snps_df.sample(n = len(snps_df), replace = True)


        ### Save the sampled SNPs data
        with open("boot_{0}.vcf".format(boot_id), "w") as outfile:
            outfile.write(header_content)
            sampled_df.to_csv(outfile, sep = "\t", header = None, index = None)
        










