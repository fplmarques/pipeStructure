#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:29:37 2020

Fernando P. L. Marques
"""
import glob
import re
from pickle import FALSE

import natsort
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def list_qfiles() -> list:
    """
    List all q-matrix files output from STRUCTURE in the current working directory.
    They all match the pattern *_q.
    """
    # Get a list of all files in the current working directory that match the pattern
    q_files = glob.glob(f"*_q")

    q_files = natsort.natsorted(q_files)

    # Return the list of matching files
    return q_files


def reorder_q_matrix(
    reference_df: pd.DataFrame, target_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Reorder the columns of the target dataframe to match the order of the reference dataframe.
    The reference dataframe is the frst one in the list of dataframes.
    """
    # Extract columns 2 to 6 from both dataframes
    ref_cols = reference_df.iloc[:, 2:].values
    target_cols = target_df.iloc[:, 2:].values

    # Calculate cosine similarity between reference and target columns
    similarities = cosine_similarity(ref_cols.T, target_cols.T)

    # Find the order of columns based on similarity
    col_order = np.argsort(-similarities, axis=0)  # Descending order

    # Reorder columns in the Target dataframe
    reordered_cols = [i + 2 for i in col_order[:, 0]]  # Add 2 for column indices in df
    reordered_target_df = target_df.iloc[
        :, [0, 1] + reordered_cols
    ]  # Include columns 0, 1

    return reordered_target_df


def compile_qmatrices_by_k() -> None:
    """
    Compile all aligned q-matrices by K value into separate files.
    """
    q_files = list_qfiles()
    is_reference = False
    for file in q_files:
        data_file = pd.read_csv(file, header=None, sep="\s+")
        # print(data_file.shape[1])
        if data_file.shape[1] == 3:
            if not is_reference:
                k_value = data_file.shape[1] - 2
                print(f" File {file} is reference for K={k_value}")
                with open("K1.tsv", mode="w") as kfile:
                    data_file.to_csv(kfile, header=False, index=False, sep="\t")
                    kfile.write("\n")
                is_reference = True
            else:
                with open("K1.tsv", mode="a") as kfile:
                    data_file.to_csv(kfile, header=False, index=False, sep="\t")
                    kfile.write("\n")
        else:
            if is_reference:
                k_value = data_file.shape[1] - 2
                print(f" File {file} is reference for K={k_value}")
                reference_dataframe = data_file
                outkfile = f"K{k_value}.tsv"
                with open(outkfile, mode="w") as kfile:
                    reference_dataframe.to_csv(
                        kfile, header=False, index=False, sep="\t"
                    )
                    kfile.write("\n")
                is_reference = False
            elif not is_reference and data_file.shape[1] == k_value + 2:
                with open(outkfile, mode="a") as kfile:
                    reordered_dataframe = reorder_q_matrix(
                        reference_dataframe, data_file
                    )
                    reordered_dataframe.to_csv(
                        kfile, header=False, index=False, sep="\t"
                    )
                    kfile.write("\n")
            else:
                k_value = data_file.shape[1] - 2
                print(f" File {file} is reference for K={k_value}")
                reference_dataframe = data_file
                outkfile = f"K{k_value}.tsv"
                with open(outkfile, mode="w") as kfile:
                    reference_dataframe.to_csv(
                        kfile, header=False, index=False, sep="\t"
                    )
                    kfile.write("\n")
                is_reference = False


def calculate_averages(file_name: str) -> pd.DataFrame:
    """
    Calculate the average values for each group in the q-matrix file.
    """
    # Read the CSV file into a dataframe
    df = pd.read_csv(file_name, header=None, sep="\t", index_col=False)

    # Calculate the average values for each group
    summary_df = df.groupby(df.columns[0]).mean().round(4)

    summary_df[1] = summary_df[1].astype(int)

    # print(summary_df.head())

    # Return the averages dataframe
    return summary_df


if __name__ == "__main__":
    print("Compiling q-matrices by K value...")
    compile_qmatrices_by_k()
    # Define the regex pattern for matching "k1.tsv", "k2.tsv", etc.
    pattern = r"K\d+\.tsv"

    # Find files that match the pattern using glob and regex
    k_files = [file for file in glob.glob("K*.tsv") if re.match(pattern, file)]

    # Sort the list of files by K value
    k_files = natsort.natsorted(k_files)

    # Calculate the average values for each group in each file
    print()
    print("Calculating average values for each group in each file...")
    for file in k_files:
        output_file = file.replace(".tsv", "_averages.tsv")
        summary_df = calculate_averages(file)
        print(f" Summarizing STRUCTURE results in {output_file}...")
        with open(output_file, mode="w") as out:
            summary_df.to_csv(out, header=False, index=FALSE, sep="\t")

    print()
    print("Done!")

exit()
