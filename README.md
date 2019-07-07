# Fileflow

File processing pipelines without boilerplate.

Fileflow combines the best design ideas from
[Luigi](https://luigi.readthedocs.io),
[Snakemake](https://snakemake.readthedocs.io), and
[Dask](https://dask.org), making it easy to create reproducable and
scalable data-analyses.
<!-- Todo: structure
1. Powerful idea of Make, Luigi, Snakemake: ..
    + DAG
    + error -> don't re-run everything
1.5: Separate work functions and pipeline definition (airflow, nextflow)
2. Normal Python code of Dask 
3. Extra: auto-generate sensible directories and filenames for intermediate
output files.
-->

<!-- To install airflow on Windows:
conda install setproctitle -c conda-forge
pip install apache-airflow
(Actually no: python-daemon is imported, nomodule named "pwd")
-->

## Installation
```
pip install fileflow
```
This will get you the
[![latest version on PyPI](https://img.shields.io/pypi/v/fileflow.svg?label=latest%20version%20on%20PyPI:)](https://pypi.python.org/pypi/fileflow/)
