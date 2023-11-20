#!/usr/bin/R
# -*- coding: utf-8 -*-
#
## This script is used to plot the results of STRUCTURE analysis
#  It requires the RColorBrewer and svglite libraries
#  Usage: Rscript plot_structure.R -i <input_file.csv>
#  The input file is a CSV from STRUCTURE analysis after summarization
#  from multiple runs using the CLUMPP software
#
#  Fernando P. L. Marques

#
## LYBRARIES
#
library(RColorBrewer)
library(svglite)

# Get the command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the input argument is provided
if(length(args) < 2 || args[1] != "-i") {
  stop("Usage: Rscript popbarplot.R -i <input_file.csv>")
}

# Read the input file from command-line argument
input_file <- args[2]
df <- read.csv(input_file, header = FALSE, sep='\t')  # Use the input_file variable
                                                      # You might need to adjust the
                                                      # separator and header settings


# Getting K value based on the number of columns. It assumes that the first two columns of the
# file are for sample and population respectively

k_value <- ncol(df) - 2	# Adjust to -1 if population assignment is not included in Structure alanysis

# Reorder the dataframe based on k_value
order_columns <- paste("df$V", 3:(k_value + 1), sep = "")
order_command <- paste("df <- df[order(", paste(order_columns, collapse = ", "), "), ]")
eval(parse(text = order_command))

# outputing graphics
output_file <- paste("k", k_value, "_barplot.svg", sep = "")

svglite(output_file, width = 12, height = 4) # Adjust the filename and dimensions

# Setting the colors
colors <- brewer.pal(n = 12, name = 'Set3')

# Plotting the barplot
#
barplot(
  t(as.matrix(df[, -(1:2)])),  # Transpose the matrix for plotting
  col = colors,
  names.arg = df$V1,   # Use the first column as x-axis labels
  xlab = "Individuals",
  ylab = "Proportion",
  main = paste("STRUCTURE ", "K =", k_value),
  cex.names = 0.5 
)

dev.off()
