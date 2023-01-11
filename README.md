# combine_csv

Based on an idea from [https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py](https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py), this small script simply focus on merging CSV/TSV files, by combining either lines or column.

Item|Project site
--|--
Source|[https://github.com/gmtsciencedev/combine_csv](https://github.com/gmtsciencedev/combine_csv)
Documentation|[https://combine_csv.readthedocs.io/](https://combine_csv.readthedocs.io/)
Download|[https://pypi.org/project/combine-csv/](https://pypi.org/project/combine-csv/)
Keywords|python, csv, merge, combine

## Basic usage

The tool can be used either :

- in line mode (default) which use all different CSV to create new lines in a merged CSV,
- or in column mode (using flag `-c`) which use all different CSV to add new columns, using the first column as an index in all files.

### Line mode

```bash
combine_csv -i '*.csv' -o my_merged_csv.csv
```

Thus if folder contains:

`1.csv`
```
name,age
Jean,23
Paul,12
```

`2.csv`
```
name,age,sex
Jane,19,female
John,74,male
```

It will create this file:
`my_merged_csv.csv`
```
name,age,sex
Jean,23,
Paul,12,
Jane,19,female
John,74,male
```

### Column mode

```bash
combine_csv -c -i '*.csv' -o my_merged_csv.csv
```

Thus if folder contains:
`1.csv`
```
task_id,name,desc
1,create,create a new object
2,delete,delete an object
```

`2.csv`
```
task_id,program
1,create.py
2,delete.py
3,random.py
```

It will create this file:
`my_merged_csv.csv`
```
task_id,name,desc,program
1,create,create a new object,create.py
2,delete,delete an object,delete.py
3,,,random.py
```

## Main options

See command line `combine_csv -h` for all options. Here we would like to point the most convinient ones. 

As you have seen `-i` is the input selector which takes a python glob.glob pattern (protect it with **single** quotes as in the examples above to prevent shell interpretation), and `-o` give the name of the file (which default to `combine.csv`)

`-s --separator`
:   Change the default field separator from `,` to whatever you need. For TSV file, say `\t` (add single quotes around to prevent backslash interpretation by shell, e.g. `-s '\t'` or `-s \\t`). This separator will be used to read input files and to write output file. You can chose to have a different output separator with `-t` option which behaves likewise.

`-a --addname`
:   Add the name of the input files (without extension). In line mode, this will add a new column named `source` (which name can be changed with `--source-column` option) containing the name of the files. In column mode, this will add the names to non-index columns preceded by an underscore.

