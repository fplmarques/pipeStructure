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
$./Rscript plot4clumpp.R -i <input_file.csv> [-o <order_file.txt>] [-t <translation_table.tsv>]"
```
### Arguments:
**-i** String specifying the input file, which is the output file from CLUMPP  containing individual Q-matrix (_e.g.,_ _K*-combined-merged.txt_ )


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

### 2. Running _preCLUMPP.py_
```bash
$./preCLUMPP.py
```
**Comment:**
- The command line above should be executed in the directory where you have your STRUCTURE results.
- For the test files above, the script will generate the following files for K ranging from 1 to 4:
  - K*_paramfile.txt
  - K*_indfile.txt
- CLUMPP's indfile have the following structure:

<pre>
```
  1        2   (56)    2 :  0.543 0.060 0.187 0.211  
  2       10    (7)    3 :  0.002 0.997 0.000 0.000  
  3       11   (35)    4 :  0.000 0.995 0.000 0.004  
...  
 20       42   (91)   11 :  0.002 0.002 0.994 0.002  
 21       45   (81)    5 :  0.068 0.028 0.893 0.011  
 22       47   (48)   14 :  0.002 0.005 0.899 0.094  
  
  1        2   (56)    2 :  0.009 0.004 0.195 0.791  
  2       10    (7)    3 :  0.999 0.001 0.000 0.000  
  3       11   (35)    4 :  0.998 0.002 0.000 0.001  
...  
 20       42   (91)   11 :  0.014 0.000 0.978 0.007  
 21       45   (81)    5 :  0.000 0.105 0.890 0.004  
 22       47   (48)   14 :  0.005 0.000 0.898 0.097  
  
  1        2   (56)    2 :  0.001 0.769 0.002 0.229  
  2       10    (7)    3 :  0.002 0.000 0.998 0.000  
  3       11   (35)    4 :  0.001 0.005 0.994 0.000  
...  
 19       41   (73)   11 :  0.160 0.009 0.003 0.828  
 20       42   (91)   11 :  0.017 0.001 0.001 0.981  
 21       45   (81)    5 :  0.018 0.002 0.089 0.891  
 22       47   (48)   14 :  0.063 0.042 0.000 0.895  
```
</pre>

  - it should have as many blocks of Q-matrices as the number of STRUCTURE replicates.

- CLUMPP's paramfile will look like this:

<pre>
```
DATATYPE 0  
INDFILE K4_indfile.txt  
POPFILE NOTNEEDED.popfile  
OUTFILE K4-combined-merged.txt  
MISCFILE K4-combined-miscfile.txt  
K 4  
C 22  
R 10  
M 2  
W 0  
S 2  
GREEDY_OPTION 2  
REPEATS 200 
PERMUTATIONFILE NOTNEEDED.permutationfile  
PRINT_PERMUTED_DATA 1  
PERMUTED_DATAFILE K4-combined-aligned.txt  
PRINT_EVERY_PERM 0  
EVERY_PERMFILE K4-combined.every_permfile  
PRINT_RANDOM_INPUTORDER 0  
RANDOM_INPUTORDERFILE K4-combined.random_inputorderfile  
OVERRIDE_WARNINGS 0  
ORDER_BY_RUN 0  
```
</pre>

- **Comments:**
  - Values for K, C, and R are assigned by the script based on parsed files.
  - K values for output files are based on examined values of K evaluated by STRUCTURE
  - All other settings can be changed as desired by the user by editing the script.

### 3. Running [CLUMPP](https://rosenberglab.stanford.edu/clumpp.html)
```bash
$ CLUMPP K4_paramfile.txt
```
- This command will generate the following files (check [CLUMPP documentation](https://rosenberglab.stanford.edu/software/CLUMPP_Manual.pdf) for details):
  - K4-combined-aligned.txt
  - K4-combined-merged.txt
  - K4-combined-miscfile.txt
- The file _K4-combined-merged.txt_ contains the individual Q-matrix computed as the mean overall individual Q-matrices after the columns have
been aligned according to the permutation with the greatest H-value. This is the file that will be used to create stacked assignment barplots.

### 4. Plotting CLUMPP's results with _plot4clumpp.R_

- The script _plot4clumpp.R_ generates stacked assignment barplots.
- **Usage**

  

![example](https://github.com/fplmarques/pipeStructure/blob/main/test_files/k4_barplot.png)




