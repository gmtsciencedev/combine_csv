# combine_csv

Based on an idea from [https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py](https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py), this small script simply focus on merging CSV/TSV files, by combining either lines or column.

Item|Project site
--|--
Source|[https://github.com/gmtsciencedev/combine_csv](https://github.com/gmtsciencedev/combine_csv)
Documentation|[https://combine-csv.readthedocs.io/](https://combine-csv.readthedocs.io/)
Download|[https://pypi.org/project/combine-csv/](https://pypi.org/project/combine-csv/)
Keywords|python, csv, merge, combine

NB starting from v3 a `combine_tsv` utility is provided, it behaves exactly the same but default to TAB as a separator.

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

NB starting from v3 a `split_tsv` utility is provided, it behaves exactly the same but default to TAB as a separator.

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
split_csv -o 'my{index}-{a}.csv' my.csv
```

Will create three files: `my1-0.csv`, `my2-0.csv` and `my3-1.csv`

# sas

*New in v3*

A `sas2csv` (resp. `sas2tsv`) utility is provided to convert SAS file (.sas7bdat) into CSV (resp TSV) files. It relies mostly on pyreadstat library that does all the work here. 

The utility takes a SAS file and a create a CSV (resp. TSV) file replacing the .sas7bdat extension by .csv (resp .tsv). You may use `-o` option to provide your own name. 

```bash
sas2csv my_sas_file.sas7bdat
```

SAS files contain both column names and column labels. By tradition column names are rather short and upper case in SAS (and may be somewhat cryptic to nowadays standards), as pyreadstat give access to both using `-l` option will enable to use labels, getting longer, more explicit names in the produced CSV file:

```bash
sas2csv -l my_sas_file.sas7bdat
```

# pivot

*New in v3*

A pivot transformation is what is called in MS Excel a dynamic table. In the input CSV file, one of the column is holding a variable name, and another one is holding a variable value. In the output TSV file, each variable name becomes a new column of its own, holding the value that was specified in the variable value column:

- input file `input.csv`:

```text
index,variable,value
1,a,11
1,b,12
1,c,13
2,a,21
2,c,23
3,b,32
```

with :
```bash
pivot_csv -p 2 -v 3 input.csv
```

- a output file called `input-pivot.csv` will be produced:
```text
index,a,b,c
1,11,12,13
2,21,,23
3,,32,
```

- `-p` option defines the position(s) that hold the name of the new columns to create. Here the value is 2, the column named `variable`.
- `-v` option defines the position(s) that hold the value(s) of the new cell to create. Here the value is 3, the column named `value`.

The first column is used as an index, the identifier of an object, to which the variable names are attribute. Thus the first line of our input file says that in object `1` the attribute `a` holds value `11`. It means that in our pivoted CSV, we will have in the line starting with `1` a column `a` with value `11`. In the second line of our input CSV, we are still on the object `1` thus it will not create a new line in our pivoted CSV, it will add extra columns to the first line. Only the fourth data line introduces a new object, the object `2` that will create a new line in our pivoted CSV.

## multiple name columns

You may define several name columns with `-p`, using a comma separated list of integer holding the different column positions (starting from 1). This means that variable names are defining combining several columns (all different name parts are aggregated, separated with a space)

For instance with input:
```text
index,variable1,variable2,value
1,a,1,11
1,b,2,12
1,c,3,13
2,a,1,21
2,c,1,23
3,b,2,32
```

The call using `pivot_csv -p 2,3 -v 4 input.csv` will generate:

```text
index,a 1,b 2,c 3,c 1
1,11,12,13,
2,21,,,23
3,,32,,
```

## multiple value columns

You may define several value columns with `-v`, using a comma separated list of integer holding the different column positions (starting from 1). This means that the the dynamic variable are composite, holding different sub-values. A new column will be created for each of these column per dynamic name, unless they hold no value. Anyway, in that case, the name of the column holding the value will be added to the dynamic name.

For instance with input:
```text
index,variable,value1,value2
1,a,1,11
1,b,2,12
1,c,3,13
2,a,1,21
2,c,1,23
3,b,2,32
```

The call using `pivot_csv -p 2 -v 3,4 input.csv` will generate:

```text
index,a value1,a value 2,b value1,b value2,c value1, c value2
1,1,11,2,12,3,12
2,1,21,,,1,23
3,,,2,32,,
```

## using range within -p or -v

For conveniance, instead of enumerating a long list, you may use a range like `1-10` which is the same as `1,2,3,4,5,6,7,8,9,10`.
You may combine ranges and simple integer, for instance `1,4-7,9-12` which is the same as `1,4,5,6,7,9,10,11,12`
You may use partial ranges like `4-` wich means `4,5,6,...` ending with the last column of the file.
You may also use negative values as in python, `-1` meaning the last column, `-2` the column just before the last column, etc., however you cannot use negative columns in range expressions.

## extra columns in input file

The algorithm defines what is to be done with: 
- the first column: this is the index, or the identifier of the object, 
- the name or pivot columns: this define the names of the new columns to create,
- the value columns: this define the values to add in the new cells.

What of other columns? They are interpreted as non dynamic attributes of the object. Non dynamic meaning here that they are not expected to vary if related to the same index or object identifier. 

For instance:
```text
index,name,variable,value
1,dog,weight,1
1,dog,length,2
2,cat,weight,1
2,cat,length,1
```

The call using `pivot_csv -p 3 -v 4 input.csv` will generate:

```text
index,name,weight,length
1,dog,1,2
2,cat,1,1
```

If the input file is instead:
```text
index,name,variable,value
1,dog,weight,1
1,dog,length,2
2,cat,weight,1
2,bird,length,1
```

The same call would generate a warning:
`Non pivoted columns hold extra information: column name [#2] contains different information from what was gathered before : 'bird' instead of 'cat', this will be discarded`

The output file would not be changed, as the `bird` information in last line is discarded.

To be complete this last input file would also give the same output as before, and without any warning as holding no value at all is not interpreted as a new input:

```text
index,name,variable,value
1,dog,weight,1
1,,length,2
2,cat,weight,1
2,,length,1
```

## pivot_tsv

As with other utility a sister utility named `pivot_tsv` is provided and it behaves exactly the same except it defaults to TSV with TAB as a separator.