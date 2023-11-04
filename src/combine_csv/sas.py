import pyreadstat
import argparse
import os

def read_sas(sasfile, separator, output, use_labels):
  """Convert a sas file to a CSV file"""
  df, meta = pyreadstat.read_sas7bdat(sasfile)
  
  if use_labels:
    if meta.column_names != list(df.columns):
      raise RuntimeError('column names do not match')
    df.columns = meta.column_labels
  df=df.set_index(df.columns[0])
  df.to_csv(output,sep=separator)


def main(default_separator=',', default_extension='.csv', file_type='CSV'):
    parser = argparse.ArgumentParser(
                    description = f"""Convert a SAS file (.sas7bdat) to a {file_type} file""")
    parser.add_argument('-s', '--separator', type=str, default=default_separator, 
        help=f'What separator to use, default to {default_separator}')
    parser.add_argument('-o', '--output', type=str, default=None, help=f'Output file (default to input file with extension replaced by {default_extension})')
    parser.add_argument('-l', '--use-labels', action='store_true',
                        help='Use SAS labels as column name instead of SAS names')
    parser.add_argument('sasfile', type=str, help='Path to SAS file')

    args = parser.parse_args()

    if args.output is None:
      args.output = os.path.splitext(args.sasfile)[0] + default_extension
    if args.separator=='\\t':
      args.separator='\t'

    read_sas(
       sasfile=args.sasfile,
       separator=args.separator,
       output=args.output,
       use_labels=args.use_labels
    )

def tsv_main():
   main(default_extension='.tsv', default_separator='\t', file_type='TSV')
