# this does the opposit of combine_csv
import argparse
import pandas as pd
import os

DEFAULT_OUTPUT_PATTERN = '{input}_{index}.{ext}'
DEFAULT_ENCODING = 'utf-8'

def split_csv(input, output_pattern, encoding, separator, output_separator, column, rename):
    """A CSV split procedure
    """
    df = pd.read_csv(input, sep=separator, index_col=0, encoding=encoding)
    basename, ext = os.path.splitext(input)
    ext = ext[1:]

    if column:
        for col in df.columns:
            filename = output_pattern.format(index=col, input=basename, ext=ext)
            this_df = df[col]
            if rename:
                this_df.name=rename
            this_df.to_csv(filename, sep=output_separator)
    else:
        for index, row in df.iterrows():
            dict = row.to_dict()
            dict.update({'index':index, 'input':basename, 'ext':ext})
            filename = output_pattern.format( **dict )
            if rename:
                row.name = rename
            pd.DataFrame(row).transpose().to_csv(filename, sep=output_separator, index_label=df.index.name)


def main(default_separator=',', file_type='CSV'):
    parser = argparse.ArgumentParser(description=f"Split one {file_type} file with into several files, either one file per line (default) or one file per column (column mode)")

    parser.add_argument("input", type=str,
                        help=f"{file_type} input file")

    parser.add_argument("-c", "--column", action="store_true",
                        help="Operate in 'column mode', that is each column will become a new two column CSV with all the lines - the first column is thought to be the index")
    parser.add_argument("-o", "--output", type=str, default=DEFAULT_OUTPUT_PATTERN,
                        help=f"""Output {file_type} file pattern (default to {DEFAULT_OUTPUT_PATTERN}). 
        The PATTERN can use python variable using the F-string syntax (with brackets).
        The variable can be either a column title (in default line mode) or index (in column mode) or input (the base name of the input file) or ext (the ext of the input file)""")
    parser.add_argument("-e", "--encoding", type=str, default=DEFAULT_ENCODING, 
                        help=f"Encoding to use (default to {DEFAULT_ENCODING})")
    parser.add_argument("-s", "--separator", type=str, default=default_separator,
                        help=f"Separator to use for input (and output unless -t is used), default to {repr(default_separator)} if set to auto then autodetection is done (slower) (use \\t quoted for tab)")
    parser.add_argument("-t", "--outputseparator", type=str, default=None,
                        help=f"Separator to use for output, default to separator option, see above, and to {repr(default_separator)} as a last resort")  
    parser.add_argument("-r","--rename", default=None, type=str,
                        help='Rename index (first word of 2nd line in line mod, second word in 1st line in column mod) to this string in resulting TSV file')
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
    

    

    split_csv(input=args.input, output_pattern=args.output, encoding=args.encoding,
                separator=args.separator, output_separator=args.outputseparator, column=args.column,
                rename=args.rename)
    
def tsv_main():
    main(default_separator='\t', file_type='TSV')