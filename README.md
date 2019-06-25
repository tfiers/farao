# Farao

File processing pipelines without boilerplate.

- Create Python functions that read from input files and write to output
  files.
- Compose them in a workflow using normal Python code, with minimal
  annotation.
- Farao auto-generates sensible names for intermediate output files, and
  runs the functions in the workflow graph:
  - In an order that respects input/output file dependencies
  - In parallel where possible
  - Making sure not to repeat previously done work

Farao combines the best design ideas from
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

Minimal workflow example:
```py
from my_tasks import downsample, calc_envelope, plot_matrix
from my_config import raw_data
from farao import schedule, run_all

envelope_files = []
for recording_file in raw_data:
    downsampled_signal_file = schedule(downsample, [recording_file])
    envelope_file = schedule(calc_envelope, [downsampled_signal_file])
    envelope_files.append(envelope_file)

schedule(plot_matrix, envelope_files)
run_all()
```

<!-- To install airflow on Windows:
conda install setproctitle -c conda-forge
pip install apache-airflow
(Actually no: python-daemon is imported, nomodule named "pwd")
-->
