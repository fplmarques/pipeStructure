# Script descriptions
## pipeStructure
- _pipeStructure.py_ automates STRUCTURE by parallelizing multiple runs. 
- The script requires STRUCTURE to be installed and available in the PATH.
- You should inspect STRUCTURE's settings for the functions that write _mainparams.txt_ and _extraparams.txt_ files to accommodate your needs.

### Requirements:
- It requires [STRUCTURE](https://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v2.3.4/html/structure.html)

### Usage:

```bash
$./pipeStructure.py [-h] -i file -k int [-o prefix] [-j int] [-r int] [--burnin int] [--numreps int]
```

### Arguments:
#### Required
**-i/--input**  Name of the structure input file (*.str, see below for details).
- The script assumes that your input file for STRUCTURE includes population data.
- Is you have only samples, you need to modify the script.

**-k/--max_k**  Integer assigning the maximum number of K to be evaluated.

### Optional
**-h/--help**  Show this help message and exit.

**-o/--output_prefix** String that specifies the prefix for STRUCTURE output files. Uses input file name if not specified.

**-j/--n_jobs int**  Integer assigning the number of nodes to spawn simultaneous processes (parallel); default is 10.

**-r/--str_rep** Integer assigning the number of replicates for each k; default is 50.

**--burnin**  Integer specifying the length of the burnin period before the start of data collection by STRUCTURE; default is 50000.

**--numreps** Interger specifying the number of MCMC reps after burnin by STRUCTURE; default is 25000.


## sumStructure
- _sumStructure.py_ summarizes the results from multiple runs and replicates of STRUCTURE by:
  - Aligning the results printed in q_matrices files and concatenating them in files according to K (_i.e.,_ K*.tsv)
  - Summarizing results in a single file by averaging cluster assignments for each sample 


## popbarplot
- _popbarplot.R_ generates barplots from summary q_matrix from STRUCTURE either generated by _sumStructure.py_.

### Usage:
```bash
$./Rscript popbarplor.R -i <input_file>
```
- The script will output a file in SVG format.

## preCLUMPP
- _preCLUMPP.py_ parses [STRUCTURE](https://web.stanford.edu/group/pritchardlab/structure.html) ***_f** [files](https://rosenberglab.stanford.edu/software/CLUMPP_Manual.pdf)
   and compile [indfile](https://rosenberglab.stanford.edu/software/CLUMPP_Manual.pdf) and [paramfile](https://rosenberglab.stanford.edu/software/CLUMPP_Manual.pdf) for [CLUMP](https://rosenberglab.stanford.edu/clumpp.html).

### Usage:
```bash
$./preCLUMPP.py
```
## plot4clumpp
- _popbarplot.R_ generates barplots from summary Q-matrix from STRUCTURE either generated by _sumStructure.py_.

### Usage:
```bash
$./Rscript plot4clumpp.R -i <K*-combined-merged.txt>
```
- _K*-combined-merged.txt_ is generated by CLUMPP after executing:

```bash
$./CLUMPP K*_paramfile.txt
```
- The script will output a file in SVG format.

### Example of plot:


![example](https://github.com/fplmarques/pipeStructure/blob/main/test_files/k2_barplot.png)

---

# Pipeline associated with the test files
### 1. Running _pipeStructure.py_

```bash
$./pipeStructure.py -i test_structure.str -k 4 -o test -j 5 -r 10 --burnin 500 --numreps 500
```

**Comment:**
- The command line above runs STRUCTURE for k values varying from 1 to 4 (**-k 4**) considering 10 replicates for each k (**-r 10**).
- STRUCTURE processes were parallelized using 5 nodes (**-j 5**).
- Output files were written with the prefix 'test' (**-o test**).
- STRUCTURE settings included **--burnin 500** and **--numreps 500** (very low numbers for demonstration only!).

As a result, 80 files were produced: 4 values of K x 10 replicates per k x 2 standard STRUCTURE outputs (*_f and *_q).

### 2. Running _sumStructure.py_
- This script is used to summarize the results of the previous section.

```bash
$./sumStructure.py
```

The execution with these test files will print:

```
Compiling q-matrices by K value...
 File test_rep_1_q is reference for K=1
 File test_rep_11_q is reference for K=2
 File test_rep_21_q is reference for K=3
 File test_rep_31_q is reference for K=4

Calculating average values for each group in each file...
 Summarizing STRUCTURE results in K1_averages.tsv...
 Summarizing STRUCTURE results in K2_averages.tsv...
 Summarizing STRUCTURE results in K3_averages.tsv...
 Summarizing STRUCTURE results in K4_averages.tsv...

Done!
```

The script created the following:
- Four files containing the aligned q_matrices for each K value: K1.tsv, K2.tsv, K3.tsv, and K4.tsv.
- Four files summarizing the results by averaging the assignment for each sample: K1_average.tsv, K2_average.tsv, K3_average.tsv, and K4_average.tsv.

### 3. Plotting the results of _sumStructure.py_ with _popbarplot.R_
- _popbarplot.R_ will plot the files containing the mean membership coefficients (Q-matrices) for K generated by _sumStructure.py_.
- For example, the command line:
```bash
$ Rscript popbarplot.R -i K4_average.tsv
```
will generate the following bar plot:




