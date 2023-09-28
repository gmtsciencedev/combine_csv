# this does the opposit of combine_csv
import argparse
import pandas as pd
import os

DEFAULT_OUTPUT_PATTERN = '{input}_{index}.{ext}'
DEFAULT_ENCODING = 'utf-8'

def split_csv(input, output_pattern, encoding, separator, output_separator, column):
    """A CSV split procedure
    """
    df = pd.read_csv(input, sep=separator, index_col=0)
    basename, ext = os.path.splitext(input)
    ext = ext[1:]

    if column:
        for col in df.columns:
            filename = output_pattern.format(index=col, input=basename, ext=ext)
            df[col].to_csv(filename, sep=output_separator)
    else:
        for index, row in df.iterrows():
            dict = row.to_dict()
            dict.update({'index':index, 'input':basename, 'ext':ext})
            filename = output_pattern.format( **dict )
            pd.DataFrame(row).transpose().to_csv(filename, sep=output_separator, index_label=df.index.name)


def main():
    parser = argparse.ArgumentParser(description="Split one CSV file with into several files, either one file per line (default) or one file per column (column mode)")

    parser.add_argument("input", type=str,
                        help="CSV input file")

    parser.add_argument("-c", "--column", action="store_true",
                        help="Operate in 'column mode', that is each column will become a new two column CSV with all the lines - the first column is thought to be the index")
    parser.add_argument("-o", "--output", type=str, default=DEFAULT_OUTPUT_PATTERN,
                        help=f"""Output CSV file pattern (default to {DEFAULT_OUTPUT_PATTERN}). 
        The PATTERN can use python variable using the F-string syntax (with brackets).
        The variable can be either a column title (in default line mode) or index (in column mode) or input (the base name of the input file) or ext (the ext of the input file)""")
    parser.add_argument("-e", "--encoding", type=str, default=DEFAULT_ENCODING, 
                        help=f"Encoding to use (default to {DEFAULT_ENCODING})")
    parser.add_argument("-s", "--separator", type=str, default=',',
                        help="Separator to use for input (and output unless -t is used), default to ',' if set to auto then autodetection is done (slower) (use \\t quoted for tab)")
    parser.add_argument("-t", "--outputseparator", type=str, default=None,
                        help="Separator to use for output, default to separator option, see above, and to , as a last resort")  
    args = parser.parse_args()

    if args.separator == 'auto':
        args.separator = None
    if args.outputseparator is None:
        if args.separator is not None:
            args.outputseparator=args.separator
        else:
            args.outputseparator=','
    
    if args.separator == '\\t':
        args.separator = '\t'
    if args.outputseparator == '\\t':
        args.outputseparator = '\t'
    

    split_csv(input=args.input, output_pattern=args.output, encoding=args.encoding,
                separator=args.separator, output_separator=args.outputseparator, column=args.column)