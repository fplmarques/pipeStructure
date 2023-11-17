# pipeStructure
- This script automates STRUCTURE by parallelizing multiple runs. 
- The script requires STRUCTURE to be installed and available in the PATH.
- You should inspect STRUCTURE's settings for the functions that write _mainparams.txt_ and _extraparams.txt_ files to accommodate your needs.

## Requirements
- It requires [Strucure](https://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v2.3.4/html/structure.html)

## Usage:

```bash
$./pipeStructure.py [-h] -i file -k int [-o prefix] [-j int] [-r int] [--burnin int] [--numreps int]
```
