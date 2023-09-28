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

- in the line mode (default) which use all different CSV to create new lines in a merged CSV,
- or in the column mode (using flag `-c`) which use all different CSV to add new columns, using the first column as an index in all files.

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

See command line `combine_csv -h` for all options. Here we would like to point the most convenient ones. 

As you have seen `-i` is the input selector which takes a python glob.glob pattern (protect it with **single** quotes as in the examples above to prevent shell interpretation), and `-o` give the name of the file (which default to `combine.csv`)

`-s --separator`
:   Change the default field separator from `,` to whatever you need. For TSV file, say `\t` (add single quotes around to prevent backslash interpretation by shells, e.g. `-s '\t'` or `-s \\t`). This separator will be used to read input files and to write the output file. You can choose to have a different output separator with the `-t` option which behaves likewise.

`-a --addname`
:   Add the name of the input files (without extension). In line mode, this will add a new column named `source` (which name can be changed with the `--source-column` option) containing the name of the files. In column mode, this will add the names to non-index columns preceded by an underscore.

# Split

## Base usage

In version 2.0 a new utility was introduced, `split_csv`, enabling to do the opposite of merging: splitting. It uses the same flags as above (-s for the input separator, -t for the output separator, -c for column mode). 

For instance, with a sample CSV `my.csv` file like this:

```text
x,a,b
1,0,1
2,0,1
3,1,0
```

Using the line mode like this:
```bash
split_csv my.csv
```

Will produce three files:

 `my_1.csv` :
```text
x,a,b
1,0,1
```

`my_2.csv` :
```text
x,a,b
2,0,1
```

`my_3.csv`:
```text
x,a,b
3,1,0
```

While using the column mode with the `-c` option:
```bash
split_csv -c my.csv
```

will produce two files:

`my_a.csv` :
```text
x,a
1,0
2,0
3,1
```

`my_b.csv`:
```text
x,b
1,1
2,1
3,0
```

## Controlling new file naming

The file naming uses a default pattern of `{input}_{index}.{ext}` which uses python F-string syntax. You can provide your own pattern with the `-o` option.
Each bracket term is dynamically replaced during splitting:

- input: input is replaced by the base name of the input file including any path if provided,
- index: index is replaced by the current name of either the column or the line depending on the mode,
- ext: ext is replaced by the extension (`csv` in the above example).

In the case of the line-split mode, the pattern may also use one of the column name: the term is replaced by the current value of the column for the line. 

For instance, in the above example:
```bash
split_csv -o 'my{index}-{a}.csv' /tmp/test1/t.csv
```

Will create three files: `my1-0.csv`, `my2-0.csv` and `my3-1.csv`