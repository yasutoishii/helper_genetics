Here, helper scripts for genetic analyses are distributed.  
If you have any questions or want to ask me anything, please contact y.ishii.biology[at]gmail.com.

# Menu
  [Scripts](#scripts): A list of scripts and brief explanation  
  [Brief usages](#brief-usages): Brief usages of the scripts  
  [Dependencies](#dependencies): Dependencies of the scripts

# Scripts
- **migrateFromNexus.py**  
  This script generates a input file for [migrate-n](https://peterbeerli.com/migrate-html5/) from a nexus file.  
  It assume that all locus are unlinked.  

- **MIGseq_qc.sh**  
  Trim adaptors and filtering by quality to assembly a MIGseq library.  
  Modify parameter values (the details of variables are written in the script).  
  For assembly with stacks, the length of filtered reads are the same; otherwise, stacks may raise an error.  
  The length is specified by `OUTPUT_LEN`.  
  In my experience, when I shortened the reads, I got more reads and loci; `OUTPUT_LEN`=100 may be good even if you have 150PE reads.  
  Note that `N_THREADS` should be set as you like (default: 15).    

- **vcf_bootstrap_rad.py**  
  This script bootstrap SNPs in a VCF file genotyped by reduced-representation sequencing (eg. RAD-seq).   

# Brief usages
- **migrateFromNexus.py**  
  ```bash
  migrateFromNexus.py -i input_file.nex -o output_file -p population_file
  ```
  The input file must be nexus format.  
  The population file discribe which population each individual is assigned to.  
  The file is tab-delimited and without a header.  
  The first column is sample IDs and the second column is population name.  
  For example:
  ```
  sample1   pop1
  sample2   pop1
  sample3   pop2
  ```  

- **MIGseq_qc.sh**  
  Usage:
  ```bash
  bash MIGseq_qc.sh
  ```

- **vcf_bootstrap_rad.py**  
  ```bash
  vcf_bootstrap_rad.py -i your.vcf -n 100 --blocked_bootstrap
  ```
  `-i`: The input VCF file  
  `-n`: # of bootstrap sampling  
  `--blocked_bootstrap`: performing blocked bootstrapping. If not specified, normal bootstraping is conducted.    


# Dependencies  
- **migrateFromNexus.py**  
  - Biopython
  - Pandas
  - argparse
