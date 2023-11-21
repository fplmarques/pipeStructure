#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script parses the output files from STRUCTURE and writes the indfile and paramfile
to be analyzed by CLUMPP .

Created on Thu Apr  2 15:29:37 2020

Fernando P. L. Marques
"""
import glob
import re

import natsort


def list_ffiles() -> list:
    """
    List all *_f output files ffrom STRUCTURE in the current working directory.
    """
    # Get a list of all files in the current working directory that match the pattern
    f_files = glob.glob(f"*_f")

    f_files = natsort.natsorted(f_files)

    # Return the list of matching files

    return f_files


def parse_file(f_file: str, previous_k: int) -> tuple:
    """
    Parse the *_f file from STRUCTURE to compile:
        - the number of samples
        - the number of clusters (K)
        - the indfile for CLUMPP
    """

    # Pattern to match lines with required information
    samples_pattern = r"   (\d+) individuals"
    current_k_pattern = r"   (\d*) populations assumed"
    pattern_clusters = r"\s+\d+\s+\d+\s+\(\d+\)\s+\d+\s+:.*"

    with open(f_file, "r") as file:
        lines = file.readlines()

        for line in lines:
            samples_match = re.match(samples_pattern, line)
            if samples_match:
                samples = int(samples_match.group(1))

            current_k_match = re.match(current_k_pattern, line)
            if current_k_match:
                current_k = int(current_k_match.group(1))

            clusters_match = re.match(pattern_clusters, line)
            if clusters_match:
                if current_k == previous_k:
                    with open(f"K{current_k}_indfile.txt", "a") as output_file:
                        output_file.write(line)
                else:
                    with open(f"K{current_k}_indfile.txt", "w") as output_file:
                        output_file.write(line)
                    previous_k = current_k
    with open(f"K{current_k}_indfile.txt", "a") as output_file:
        output_file.write("\n")
    return samples, current_k


def write_CLUMPP_paramfile(current_k: int, n_samples: int, n_replicates: int) -> None:
    """
    Write CLUMPP paramfile to current working directory.
    """
    # Define struct_extraparams of output file
    clumpp_paramfile = f"""DATATYPE 0 
INDFILE K{current_k}_indfile.txt
POPFILE NOTNEEDED.popfile 
OUTFILE K{current_k}-combined-merged.txt 
MISCFILE K{current_k}-combined-miscfile.txt 
K {current_k}       # Number of clusters.
C {n_samples}       # Number of individuals/populations.
R {n_replicates}    # Number of replicates/runs of Structure.
M 2                 # Choice of algorithm (1 = FullSearch, 2 = Greedy, 3 = LargeKGreedy).
W 0                 # Procedure for weighting by the number of individuals (1 = weight by number of individuals, 0 = weight each line equally). If DATATYPE = 0, this option is automatically set to 0.
S 2                 # Choice of pairwise matrix similarity statistic (1 for G and 2 for G0).
GREEDY_OPTION 2 
REPEATS 200
PERMUTATIONFILE NOTNEEDED.permutationfile 
PRINT_PERMUTED_DATA 1 
PERMUTED_DATAFILE K{current_k}-combined-aligned.txt 
PRINT_EVERY_PERM 0 
EVERY_PERMFILE K{current_k}-combined.every_permfile 
PRINT_RANDOM_INPUTORDER 0 
RANDOM_INPUTORDERFILE K{current_k}-combined.random_inputorderfile 
OVERRIDE_WARNINGS 0 
ORDER_BY_RUN 0 """

    # Write structure mainparams to output file
    with open(f"K{current_k}_paramfile.txt", "w") as file:
        file.write(clumpp_paramfile)


def main():
    list_of_f_files = list_ffiles()
    count_runs = len(list_of_f_files)
    print(f"Found {count_runs} runs. Start parsing...")
    previous_k = 0

    #
    print(f"  Parsing file: {list_of_f_files[0]}")
    n_samples, current_k = parse_file(list_of_f_files[0], previous_k)
    previous_k = current_k
    list_of_Ks = [current_k]
    for f_file in list_of_f_files[1:]:
        print(f"  Parsing file: {f_file}")
        _, current_k = parse_file(f_file, previous_k)
        previous_k = current_k
        list_of_Ks.append(current_k) if not current_k in list_of_Ks else None

    n_replicates = int(count_runs / current_k)
    print("\n")
    print("######## Summary ########")
    print(f" Samples: {n_samples}")
    print(f" Ks evaluated: {list_of_Ks[-1]}")
    print(f" Number of replicates: {n_replicates}")
    print("#########################")
    print("\n")
    print("Writing CLUMPP paramfile...")
    for k in list_of_Ks:
        print(f" Writting paramfile: K{k}_paramfile.txt ...")
        write_CLUMPP_paramfile(k, n_samples, n_replicates)

    print("\n")
    print("Done!")


if __name__ == "__main__":
    main()
