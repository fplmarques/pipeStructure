# Test files
## Command lines associated with the files in the directory:
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

### 1. Running _sumStructure.py_
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
