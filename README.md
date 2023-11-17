# pipeStructure
- This script automates STRUCTURE by parallelizing multiple runs. 
- The script requires STRUCTURE to be installed and available in the PATH.
- You should inspect STRUCTURE's settings for the functions that write _mainparams.txt_ and _extraparams.txt_ files to accommodate your needs.

## Requirements:
- It requires [Structure](https://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v2.3.4/html/structure.html)

## Usage:

```bash
$./pipeStructure.py [-h] -i file -k int [-o prefix] [-j int] [-r int] [--burnin int] [--numreps int]
```

## Required arguments:

**-h/--help**  Show this help message and exit. \
**-i/--input**  Name of the structure input file (*.str, see below for details)

  
  -i file, --input file
                        Name of the structure input file (*.str).
  -k int, --max_k int   Integer assigning the maximum number of K to be evaluated.
  -o prefix, --output_prefix prefix
                        Prefix for STRUCTURE output files. Uses input file name if not specified.
  -j int, --n_jobs int  Integer assigning number of nodes to spawn simultaneous processes (parallel); default is 10.
  -r int, --str_rep int
                        Integer assigning the number of replicates for each k; default is 50.
  --burnin int          Integer specifying the length of the burnin period before the start of data collection by STRUCTURE; default is 50000.
  --numreps int  
