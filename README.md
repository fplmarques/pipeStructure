# pipeStructure
- _pipeStructure.py_ automates STRUCTURE by parallelizing multiple runs. 
- The script requires STRUCTURE to be installed and available in the PATH.
- You should inspect STRUCTURE's settings for the functions that write _mainparams.txt_ and _extraparams.txt_ files to accommodate your needs.

## Requirements:
- It requires [Structure](https://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v2.3.4/html/structure.html)

## Usage:

```bash
$./pipeStructure.py [-h] -i file -k int [-o prefix] [-j int] [-r int] [--burnin int] [--numreps int]
```

## Arguments:
### Required
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


# sumStructure
- _sumStructure.py_ summarizes the results from multiple runs and replicates of STRUCTURE by:
  - Aligning the results printed in q_matrices files and concatenating them in files according to K (_i.e.,_ K*.tsv)
  - Summarizing results in a single file by averaging cluster assignments for each sample 

