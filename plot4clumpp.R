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

#
## FUNCTIONS
#

generate_custom_plot <- function(k_value,las_val,cex_axis) {
  output_file <- paste("k", k_value, "_barplot.svg", sep = "")

  svglite(output_file, width = 12, height = 4) # Adjust the filename and dimensions

  colors <- brewer.pal(n = 12, name = 'Set3')

  barplot(
    t(as.matrix(df[, -(1:5)])),  # Transpose the matrix for plotting
    col = colors,
    names.arg = df$V2,   # Use the first column as x-axis labels
    xlab = "Individuals",
    ylab = "Proportion",
    main = paste("STRUCTURE ", "K =", k_value),
    cex.names = 0.5,
    las = las_val,
    cex.axis = cex_axis
  )
  
  dev.off() # Close the SVG device
}




# Get the command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the input argument is provided
if(length(args) < 2 || args[1] != "-i") {
  stop("Usage: Rscript plot4clumpp.R -i <input_file.csv> [-o <order_file.txt>] [-t <translation_table.tsv>]")
}

# Read the input file from command-line argument
input_file <- args[2]
df <- read.table(input_file, header = FALSE, sep = "", fill = TRUE)  # Use the input_file variable
                                                      # You might need to adjust the
                                                      # separator and header settings


# Getting K value based on the number of columns. It assumes that the first two columns of the
# file are for sample and population respectively

k_value <- ncol(df) - 5	# 

# Reorder the dataframe based on k_value
order_columns <- paste("df$V", 6:(k_value + 4), sep = "")
order_command <- paste("df <- df[order(", paste(order_columns, collapse = ", "), "), ]")
eval(parse(text = order_command))

# Check if '-o' argument is provided
if ('-o' %in% args) {
  # Get the index of the '-o' argument
  index <- which(args == '-o')
  
  # Get the file name after the '-o' argument
  file_name <- args[index + 1]
  
  # Read the file with the specified order
  specific_order <- readLines(file_name)
  
  # df$V2 is reordered based on the order of the specific_order vector
  df$V2 <- factor(df$V2, levels = specific_order)
  
  # Reorder the DataFrame based on the factor order of df$V2
  df <- df[order(df$V2), ]

}

# Check if '-t' argument is provided
if ('-t' %in% args) {
  # Get the index of the '-t' argument
  index <- which(args == '-t')
  
  # Get the file name after the '-t' argument
  file_name <- args[index + 1]
  
  # Read the translation table
  translation_table <- read.table(file_name, header = FALSE, sep = "\t", stringsAsFactors = FALSE)
  
  # Assuming df$V2 is the column you want to translate
  if ('V2' %in% colnames(df) && all(df$V2 %in% translation_table$V1)) {
    translation_index <- match(df$V2, translation_table$V1)
    df$V2 <- translation_table$V2[translation_index]

    generate_custom_plot(k_value,las_val = 2 ,cex_axis = 0.8)

    cat("Translation completed. Barplot renamed X axe accordingly.\n")
  
  } else {
    cat("Column 'V2' not found or values not matching in the translation file. Translation cannot be performed.\n")
    # Proceed without translation
    # Continue with your plotting or operations using the original DataFrame

    generate_custom_plot(k_value,las_val = 0 ,cex_axis = 1)

  }
} else {
  cat("No translation file provided. Proceeding without translation.\n")
  # Proceed without translation
  # Continue with your plotting or operations using the original DataFrame

  generate_custom_plot(k_value,las_val = 0 ,cex_axis = 1)

}

cat ("Done!\n")