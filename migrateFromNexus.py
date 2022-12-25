#!/usr/bin/env python

from Bio.Nexus.Nexus import Nexus
import pandas as pd
import argparse

def get_args():
    psr  = argparse.ArgumentParser(
        prog="migrateFromNexus.py",
        usage="migrateFromNexus.py [options]",
        description="This script generate a input file for Migrate-n from nexus."
    )

    psr.add_argument('-i',
                     '--input',
                     help="[Mandatory] Specify a input nexus file.",
                     required=True)
    psr.add_argument('-p',
                     '--popfile',
                     help="[Mandatory] Specify a population file."+
                          "Tab-delimited file. No header."+
                          "1st column: sample ID; 2nd column: population name.",
                     required=True) 
    psr.add_argument('-o',
                     '--output',
                     help="[Mandatory] Specify a output file name.",
                     required=True)
    psr.add_argument('-l',
                     '--isloud',
                     help="[Optional; Default=True] Should print log? [True, False]",
                     default=True)
    args = psr.parse_args()
    
    return args

class nexus2migration:
    def __init__(self,
                 seq_file,
                 pop_file,
                 output_file,
                 is_loud):
        ### Parameters ###
        self.seq_file = seq_file    # Input nexus file
        self.pop_file = pop_file    # Population file
        self.output_file = output_file    # Output file
        self.is_loud = is_loud    # Whether print log?
        
        ### Objects ###
        self.seq_dat = Nexus()
        self.seq_dat.read(seq_file)
        if self.is_loud:
            print("The sequence file is loaded.")
        self.pop_df = pd.read_csv(self.pop_file, header = None,
                                  names = ["id", "pop"], sep = "\t")
            
    def convert(self):
        done_len_warning = False
        locus_nams = self.seq_dat.charsets.keys()
        output_str = "   {0} {1} Title\n".format(len(self.pop_df["pop"].unique()),
                                                 len(self.seq_dat.charsets))    # header
        ### Error checker ###
        if self.seq_dat.unaltered_taxlabels != self.pop_df["id"].tolist():
            print("Error: No of samples do not match in the sequence file and"+
                  "the population file!")
            exit()

        if self.is_loud:
            print("No of locus is: {0}".format(len(locus_nams)))
            print("No of population is: {0}".format(len(self.pop_df["pop"].unique())))
            print("No of indivs is: {0}".format(len(self.pop_df)))

        for locus_nam in locus_nams:
            seq_len = (int(self.seq_dat.charsets[locus_nam][-1]) -
                       int(self.seq_dat.charsets[locus_nam][0]) + 1)
            output_str += "(s{0})".format(seq_len) + "  "
        output_str += "\n"

        for pop in self.pop_df["pop"].unique():
            n_samp_pop = len(self.pop_df[self.pop_df["pop"]==pop])
            output_str += "{0}  {1}\n".format(n_samp_pop, pop)
            ids = self.pop_df[self.pop_df["pop"]==pop]["id"]

            for id in ids:
                if len(id) > 10:
                    id10 = id[0:10].ljust(10)
                    if not done_len_warning:
                        if self.is_loud:
                            print("Warning: Sample IDs longer than 10 characters"+
                                  "will be shortened to 10 characters.")
                            done_len_warning = True
                else:
                    id10 = id.ljust(10)
                output_str += id10 + " "

                for locus_nam in locus_nams:
                    output_str += str(self.seq_dat.matrix[id]
                                      [self.seq_dat.charsets[locus_nam][0]:
                                       self.seq_dat.charsets[locus_nam][-1]+1]) + " "
                output_str += "\n"
        return output_str
                
    def save(self, output_str):
        with open(self.output_file, mode='w') as f:
            f.write(output_str)

if __name__ == '__main__':
    args = get_args()
    conv_obj = nexus2migration(args.input,
                               args.popfile,
                               args.output,
                               args.isloud)
    output_str = conv_obj.convert()
    conv_obj.save(output_str)
    
    
    
        
    
        
    
