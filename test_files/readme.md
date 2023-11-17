# Test files
## Command line associated with files:
### Running _pipeStructure.py_:

```bash
./pipeStructure.py -i test_structure.str -k 4 -o test -j 5 -r 10 --burnin 500 --numreps 500
```

**Comment:**
- The command line above runs STRUCTURE for k values varying from 1 to 4 (**-k 4**) considering 10 replicates for each k (**-r 10**).
- STRUCTURE processes were parallelized using 5 nodes (**-j 5**).
- Output files were written with the prefix 'test' (**-o test**).
- STRUCTURE settings included **--burnin 500** and **--numreps 500** (very low numbers for demonstration only!).

As a result, 80 files were produced: 4 values of K x 10 replicates per k x 2 standard STRUCTURE outputs (*_f and *_q).
