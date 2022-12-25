Here, helper scripts for genetic analyses are distributed.  
If you have any questions or want to ask me anything, please contact y.ishii.biology[at]gmail.com.

# Menu
  [Scripts](#scripts): A list of scripts and brief explanation.  
  [Brief usages](#brief-usages): Brief usages of the scripts.

# Scripts
- **migrateFromNexus.py**  
  This script generates a input file for [migrate-n](https://peterbeerli.com/migrate-html5/) from a nexus file.  
  It assume that all locus are unlinked.  

# Brief usages
- **migrateFromNexus.py**  
  ```bash
  migrateFromNexus.py -i input_file.nex -o output_file -p population_file
  ```
  The input file must be nexus format.  
  The population file discribe which population each individual is assigned to.  
  The file is tab-delimited and without a header.  
  The first column is sample IDs an the second column is population name.  
  For example:
  ```
  sample1   pop1
  sample2   pop1
  sample3   pop2
  ```  


