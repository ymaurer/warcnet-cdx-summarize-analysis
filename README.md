# Warcnet reports from cdx-summary files
These programs aim to produce reproducible statistics from summary files.

# warcnetstats.py
```
usage: warcnetstats.py [-h] [--prefix PREFIX] [--minyear MINYEAR] [--maxyear MAXYEAR] [--delimiter DELIMITER] file

Calculate Warcnet chapter statistics from summary file

positional arguments:
  file                  summary file

optional arguments:
  -h, --help            show this help message and exit
  --prefix PREFIX       prefix of the output file
  --minyear MINYEAR     Minimum Year for statc: Number of distinct domains on TLDs per year report
  --maxyear MAXYEAR     Maximum Year for statc: Number of distinct domains on TLDs per year report
  --delimiter DELIMITER
                        Output file delimiter for csv files
```
It produces the following files:
* PREFIX-stata-distinct-domains-overall.csv
* PREFIX-stata-distinct-domains-per-year.csv
* PREFIX-statb-distinct-tld-overall.csv
* PREFIX-statb-distinct-tld-per-year.csv
* PREFIX-statc-distinct-lvl2-per-tld-overall.csv
* PREFIX-statc-distinct-lvl2-per-tld-per-year.csv

## stat a)
Total number of distinct second-level domains in the summary file.

## stat b)
Total number of distinct TLDs.

## stat c)
Number of distinct domains on TLDs.
