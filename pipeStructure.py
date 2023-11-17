#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Apr  2 15:29:37 2020

This script automates STRUCTURE runs in parallel

Fernando Marques
"""

import argparse
import multiprocessing
import os
import random
import subprocess
from itertools import count
from pdb import run

#
## FUNCTIONS
#


def get_file_stats(input_str_file: str) -> (int, int):
    """
    Get the number of terminals and the number of loci from the input file.
    This is required to configure the command line for Structure
    """

    with open(input_str_file, "r") as file:
        # Get the number of lines
        num_terminals = int(sum(1 for line in file) / 2)

        # Reset file pointer to the beginning of file
        file.seek(0)

        # Get the number of loci by examining the first line and deleting the first 2 characters
        # It assumes that you are running Structure with sample and population data
        first_line = file.readline().strip()
        number_of_loci = len(first_line.split()) - 2

    return num_terminals, number_of_loci


def generate_extraparams_file(n: int) -> None:
    """
    Generate extraparams file for STRUCTURE run
    This is numbered to control parallel spawning of processes
    It also generates a SEED for each extraparams file
    You consider tailoring this function to your needs as it was
    designed to accommodate population data for Kestimator.
    """

    # Generate a random 9-digit number for seed
    seed = random.randint(100000000, 999999999)

    # Define struct_extraparams of output file
    struct_extraparams = f"""#define INFERLAMBDA         0                  //
#define POPSPECIFICLAMBDA   0            //
#define LAMBDA              1.0                       // 
             
#define FPRIORMEAN          0.01                   //
#define FPRIORSD            0.05                     // 
#define UNIFPRIORALPHA      1               // 
#define ALPHAMAX            10.0                     // 
#define ALPHAPRIORA         1.0                  // 
#define ALPHAPRIORB         2.0                  //
#define LOG10RMIN           -4.0                    //
#define LOG10RMAX           1.0                    //
#define LOG10RPROPSD        0.1                 //
#define LOG10RSTART         -2.0                  //

#define GENSBACK            2                      //
#define MIGRPRIOR           0.01                      //
#define PFROMPOPFLAGONLY    0              //

#define LOCISPOP            1                      //
#define LOCPRIORINIT        1.0                  //
#define MAXLOCPRIOR         20.0                   //

#define PRINTNET            1                     // 
#define PRINTLAMBDA         1                  //
#define PRINTQSUM           0                    //
#define SITEBYSITE          0                   // 
#define PRINTQHAT           1                    // 
#define UPDATEFREQ          10000                   // 
#define PRINTLIKES          0                   // 
#define INTERMEDSAVE        0                 //
#define ECHODATA            0                     // 
#define ANCESTDIST          0                   // 
#define NUMBOXES            1000                     // 
#define ANCESTPINT          0.9                   // 

#define COMPUTEPROB         1                    //
#define ADMBURNIN           {args.burnin}                      // 
#define ALPHAPROPSD         0.025                    // 
#define STARTATPOPINFO      0                 //
#define RANDOMIZE           0                      //
#define SEED                {seed}                           //
#define METROFREQ           10                 // 
#define REPORTHITRATE       0                  //"""

    # Write structure extraparams to output file
    with open(f"extraparams_{n}.txt", "w") as file:
        file.write(struct_extraparams)


def generate_mainparams_file(burnin=50000, n_reps=25000) -> None:
    """
    Generate mainparams file for STRUCTURE run
    The only parameters that this function controls are burnin and n_reps
    You consider tailoring this function to your needs as it was
    designed to accommodate population data for Kestimator.
    """
    # Define struct_extraparams of output file
    struct_mainparams = f"""#define BURNIN         {burnin}                  //
#define NUMREPS        {n_reps}                  //

#define PLOIDY         2                   //
#define MISSING        -9                  //
#define ONEROWPERIND   0              //

#define LABEL          1                     //
#define POPDATA        1                   //
#define POPFLAG        0                   //
#define LOCDATA        0                   //
#define PHENOTYPE      0                 //
#define EXTRACOLS      0                 //

#define MARKERNAMES       0           //
#define RECESSIVEALLELES  0      //
#define MAPDISTANCES      0          //
#define PHASED            0                //
#define PHASEINFO         0             //
#define MARKOVPHASE       0           //
#define NOTAMBIGUOUS      -999          //"""

    # Write structure mainparams to output file
    with open("mainparams.txt", "w") as file:
        file.write(struct_mainparams)


def run_structure(
    run: int,
    k: int,
    number_of_loci: int,
    num_terminals: int,
    input_str_file: str,
    output_prefix: str,
) -> None:
    generate_extraparams_file(run)
    command = f"structure -m mainparams.txt -e extraparams_{run}.txt -K {k} -L {number_of_loci} -N {num_terminals} -i ./{input_str_file} -o ./{output_prefix}_rep_{run}"
    print(f"Run {run}: [K={k}, Rep={run}] -> {command}")
    subprocess.run(command, shell=True, check=True)


def get_arguments():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="""This script automates STRUCTURE by parallelizing multiple runs.
                       The script requires STRUCTURE to be installed and available in the PATH. 
                       You should inspect STRUCTURE's settings for the functions that write
                       mainparams.txt and extraparams.txt files to accommodate your needs."""
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_str_file",
        metavar="file",
        required=True,
        help="Name of the structure input file (*.str).",
    )
    parser.add_argument(
        "-k",
        "--max_k",
        dest="max_k",
        metavar="int",
        required=True,
        type=int,
        help="Integer assigning the maximum number of K to be evaluated.",
    )
    parser.add_argument(
        "-o",
        "--output_prefix",
        dest="output_prefix",
        metavar="string",
        default=None,
        help="String that specifies the prefix for STRUCTURE output files. Uses input file name if not specified.",
    )
    parser.add_argument(
        "-j",
        "--n_jobs",
        dest="n_jobs",
        metavar="int",
        default=10,
        type=int,
        help="Integer assigning the number of nodes to spawn simultaneous processes (parallel); default is 10.",
    )
    parser.add_argument(
        "-r",
        "--str_rep",
        dest="n_struct_replicates",
        metavar="int",
        default=50,
        type=int,
        help="Integer assigning the number of replicates for each k; default is 50.",
    )
    parser.add_argument(
        "--burnin",
        dest="burnin",
        metavar="int",
        default=50000,
        type=int,
        help="Integer specifying the length of burnin period before the start of data collection by STRUCTURE; default is 50000.",
    )
    parser.add_argument(
        "--numreps",
        dest="n_reps",
        metavar="int",
        default=25000,
        type=int,
        help="Integer specifying the number of MCMC reps after burnin by STRUCTURE; default is 25000.",
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # Get command line arguments
    args = get_arguments()

    # Get file stats
    num_terminals, number_of_loci = get_file_stats(args.input_str_file)
    print(f"Number of Terminals: {num_terminals}")
    print(f"Number of Loci: {number_of_loci}")

    # Set output prefix
    if args.output_prefix is None:
        args.output_prefix = os.path.splitext(args.input_str_file)[0]

    # Generate mainparams file
    generate_mainparams_file(args.burnin, args.n_reps)

    # Create a pool of n_jobs processes
    pool = multiprocessing.Pool(processes=args.n_jobs)

    # Map the nested for loops to the pool of processes
    run = 1
    for k in range(1, args.max_k + 1):
        for replicate in range(1, args.n_struct_replicates + 1):
            pool.apply_async(
                run_structure,
                args=(
                    run,
                    k,
                    number_of_loci,
                    num_terminals,
                    args.input_str_file,
                    args.output_prefix,
                ),
            )
            run += 1

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()
