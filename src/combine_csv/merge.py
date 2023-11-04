#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#original id: https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052
#modified for GMT Science by Raynald de Lahondes

import os
import glob
import pandas as pd
import argparse


ENCODING_DEFAULT = "utf-8-sig"
SOURCE_COLUMN_NAME = "source"
ALTERNATE_COLUMN_NAME = "_source"

def combine_csv(input_pattern, output_filename, encoding, addname, separator, output_separator, column, source_column,
        sort_columns, output_encoding):
    """Find all files matching input_pattern and combine them in a unique csv named output_filename

    encoding is the encoding used to create the new file
    addname is an option to add each input file name in the resulting CSV file (see source_column for the name of the column)
    separator is the input (and output) separator for pd import (None mean use python sniffer, that is automatic)
    output_separator is the output seperator for pd export
    source_column is the name of the column where the input file name (cf addname)

    column if then the files have all an almost common column, the first, that is an index, and combine_csv will try to merge
        lines that are identical on this first column, each file combined adding extra columns, either with the name of the file added
        if addname is on, or with column name, added with a number in case it already exists. 
    """
    #find all csv files in the folder
    all_filenames = [i for i in glob.glob(input_pattern)]

    #combine all files in the list
    if column:
        data_set = None
        for f in all_filenames:
            base_name = os.path.splitext(os.path.basename(f))[0]
            if separator is None:
                data = pd.read_csv(f, index_col=0, sep=separator, engine='python', encoding=encoding)
            else:
                data = pd.read_csv(f, index_col=0, sep=separator, encoding=encoding)
            if addname:
                #data.columns = [data.columns[0]]+['{}_{}'.format(col, base_name) for col in data.columns[1:]]
                data.columns = ['{}_{}'.format(base_name,col) for col in data.columns]
            if data_set is None:
                data_set = [data]
                index_name = data.index.name
                #data_set = data
            else:
                #data_set = data_set.merge(data, left_on=data_set.columns[0], right_on=data.columns[0], copy=False, how='outer',
                #    suffixes=(None, '_extra'), validate='1:1')
                #data_set = data_set.merge(data, left_on=data_set.columns[0], right_on=data.columns[0], copy=False, how='outer',
                #    suffixes=(None, '_extra'), validate='1:1')
                data_set.append(data)
        combined_csv = pd.concat(data_set, join='outer', axis=1, sort=True)
        if sort_columns:
            combined_csv = combined_csv[sorted(combined_csv)]
        #combined_csv = data_set
        #export to csv
        combined_csv.to_csv( output_filename, sep=output_separator, index=True, index_label=index_name, encoding=output_encoding)
    else:
        if addname:
            data_set = []
            source_column_added = False
            source_column_name = source_column
            for f in all_filenames:
                base_name = os.path.splitext(os.path.basename(f))[0]
                data = pd.read_csv(f, sep=separator, encoding=encoding)
                # this is a hack to allow for incremental adding
                if f!=output_filename:
                    try:
                        data.insert(0,source_column_name,base_name)
                    except ValueError:
                        if source_column != ALTERNATE_COLUMN_NAME and not source_column_added:
                            try:
                                source_column_name = ALTERNATE_COLUMN_NAME
                                data.insert(0,source_column_name,base_name)
                            except ValueError:
                                print('This is likely because a {} column already exists (or {})'.format(
                                    source_column, ALTERNATE_COLUMN_NAME
                                ))
                                print('Try option --source-column')
                                raise
                        else:
                            print('This is likely because a {} column already exists (or {})'.format(
                                source_column, ALTERNATE_COLUMN_NAME
                            ))
                            print('Try option --source-column')
                            raise
                    source_column_added = True
                data_set.append(data)
            combined_csv = pd.concat(data_set)
        else:
            combined_csv = pd.concat([pd.read_csv(f, sep=separator, encoding=encoding) for f in all_filenames ])

        if sort_columns:
            combined_csv = combined_csv[sorted(combined_csv)]

        #export to csv
        combined_csv.to_csv( output_filename, sep=output_separator, index=False, encoding=output_encoding)

def main(default_separator=',', file_type='CSV', output_default='combined.csv', input_default='*.csv'):
    parser = argparse.ArgumentParser(description=f"Merge several {file_type} files with header, merged on the base of common columns, each file add some extra lines (except in column mode, see below)")

    parser.add_argument("-i", "--input", type=str, default=input_default,
                        help=f"{file_type} input files to combine (dont forget to quote to avoid shell interpretation of *) (default to {input_default})")
    parser.add_argument("-o", "--output", type=str, default=output_default,
                        help=f"Output {file_type} file (default to {output_default})")
    parser.add_argument("-e", "--encoding", type=str, default=ENCODING_DEFAULT, 
                        help="Input encoding, used to read (default to {})".format(ENCODING_DEFAULT))
    parser.add_argument("-E", "--output-encoding", type=str, default=None, 
                        help="Output encoding used to write output (default to input encoding)")
    parser.add_argument("-a", "--addname", action="store_true",
                        help="Add a column with source CSV file basename (not present by default)")
    parser.add_argument("-s", "--separator", type=str, default=default_separator,
                        help=f"Separator to use for input (and output unless -t is used), default to {repr(default_separator)} if set to auto then autodetection is done (slower) (use \\t quoted for tab)")
    parser.add_argument("-C", "--sort-columns", action="store_true",
                        help="Sort columns")
    parser.add_argument("-t", "--outputseparator", type=str, default=None,
                        help=f"Separator to use for output, default to separator option, see above, and to {repr(default_separator)} as a last resort")  
    parser.add_argument("-c", "--column", action="store_true",
                        help="Operate in 'column mode', that is, lines will be merged (first column is supposed to be a common key), and column will be added, with filename added if -a is used, and with _extra in case column overlapp")
    #parser.add_argument("-u", "--unsort")
    parser.add_argument("--source-column", type=str, default=SOURCE_COLUMN_NAME,
                        help="Chose source column name (only usefull with -a), default to {} - will try {} in case this is used".format(
                            SOURCE_COLUMN_NAME, ALTERNATE_COLUMN_NAME))

    args = parser.parse_args()

    if args.separator == 'auto':
        args.separator = None
    elif args.separator == '\\t':
        args.separator = '\t'

    if args.outputseparator is None:
        if args.separator is not None:
            args.outputseparator=args.separator
        else:
            args.outputseparator=default_separator
    if args.output_encoding is None:
        args.output_encoding = args.encoding
    

    combine_csv(input_pattern=args.input, output_filename=args.output, encoding=args.encoding, addname=args.addname,
                separator=args.separator, output_separator=args.outputseparator, column=args.column, 
                source_column=args.source_column, sort_columns=args.sort_columns, output_encoding=args.output_encoding)
    
def tsv_main():
    main(default_separator='\t', file_type='TSV', input_default='*.tsv', output_default='combined.tsv')