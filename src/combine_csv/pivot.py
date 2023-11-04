import pandas as pd
import argparse
import os
import logging as log



def pivot_df(df, pcols, vcols):
    """Do a pivot transformation on a dataframe, a transformation that is reminiscent of dynamic tables in MS Excel
    - df is a pandas Dataframe,
    - pcols and vcols are list of integers defining the column positions in the dataframe,
    - pcols (pivot columns) define a dynamic column name that value(s) are set in vcols (value columns),
    - the first column is treated as an index (that might be repeated due to the dynamic nature of the df)
    - other columns (not index, pcols, vcols) should not contain different informations if they are relate to the same index (will generate a warning)
    """

    
    new_df = []
    current_item = None
    new_row = {}
    one_value = len(vcols)==1

    for _,row in df.iterrows():
        labels = row.index
        item = row.iloc[0]
        if current_item != item:
            if current_item is not None:
                new_df.append(new_row)
            current_item=row.iloc[0]
            new_row = {}
            for i in range(len(row)):
                if i not in pcols and i not in vcols:
                    if not pd.isna(row.iloc[i]):
                        new_row[labels[i]]=row.iloc[i]
        else:
            for i in range(len(row)):
                if i not in pcols and i not in vcols:
                    if not pd.isna(row.iloc[i]) and labels[i] in new_row and new_row[labels[i]]!=row.iloc[i]:
                        log.warning(f'Non pivoted columns hold extra information: column {labels[i]} [#{i+1}] contains different information from what was gathered before : {repr(row.iloc[i])} instead of {repr(new_row[labels[i]])}, this will be discarded')
        column_name = ' '.join(row.iloc[pcols])
        
        if one_value:
            new_row[column_name]=row.iloc[vcols[0]]
        else:
            for i in vcols:
                new_row[f"{column_name} {labels[i]}"]=row.iloc[i]
    
    if new_row:
        new_df.append(new_row)
    
    return pd.DataFrame(new_df).set_index(labels[0])
        



def proceed_column_list(l, col_number):
    """Convert a comma separated representation of list of integer 
    (including ranges) into a list of integer"""
    new_l = []
    for e in l.split(','):
        e=e.strip()
        if e.startswith('-'):
            new_l.append(col_number+int(e)+1)
        elif e.endswith('-'):
            new_l.extend(range(int(e[:-1]), col_number+1))
        elif '-' in e:
            a,b = map(int,e.split('-'))
            new_l.extend(range(a,b+1))
        else:
            new_l.append(int(e))
    return new_l

def minus1(x):
    """Remove 1 to all items of a list of number"""
    return [i-1 for i in x]

def main(default_separator=',', file_type='CSV'):
    parser = argparse.ArgumentParser(
                    description = f"""Pivot a {file_type} file, in the manner of a dynamic table of MS Excel.
        - The first column of the file is treated as an index.
        - There may be non dynamic columns in the {file_type} file, but they should not vary for the same index (will generate a warning and value will be discarded)""")
    parser.add_argument('-p', '--pivot-columns', type=str, 
        help='A comma separated list of columns number (first column is 1) or (complete or partial) ranges with a dash ("-") that hold the name of variable to implement')
    parser.add_argument('-v', '--value-columns', type=str, 
        help='A comma separated list of columns number (first column is 1) or (complete or partial) ranges with a dash ("-") that hold the values of variable to implement')
    parser.add_argument('-s', '--separator', type=str, default=default_separator, 
        help=f'What separator to use, default to {repr(default_separator)}')
    parser.add_argument("-t", "--outputseparator", type=str, default=None,
                        help=f"Separator to use for output, default to separator option, see above, and to {repr(default_separator)} as a last resort")  
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file (default to input file with -pivot added)')
    parser.add_argument('tsvfile', type=str, help='Path to TSV file')

    args=parser.parse_args()
    if args.output is None:
        name,ext=os.path.splitext(args.tsvfile)
        args.output = f"{name}-pivot{ext}"
    if args.separator=='\\t':
        args.separator='\t'
    df = pd.read_csv(args.tsvfile, sep=args.separator)
    args.pivot_columns=minus1(proceed_column_list(args.pivot_columns, col_number=len(df.columns)))
    args.value_columns=minus1(proceed_column_list(args.value_columns, col_number=len(df.columns)))

    if args.outputseparator is None:
        if args.separator is not None:
            args.outputseparator=args.separator
        else:
            args.outputseparator=default_separator

    pivot_df(
        df=df, 
        pcols=args.pivot_columns, 
        vcols=args.value_columns, 
    ).to_csv(args.output, sep=args.outputseparator)


def tsv_main():
    main(default_separator='\t', file_type='TSV')