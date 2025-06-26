import argparse

from mace_aze.config import (
    split_methods,
    uniform_key
)
from mace_aze.pipe.file_handling.splitter import splitter

def arg_parse():
    parser = argparse.ArgumentParser(description="Splits single config file to muliple based on selection method")
    parser.add_argument('-f','-F','--file', type=str, required=True, help="Input file")
    parser.add_argument('-m', '-M', '--method', type=str, choices=split_methods, default=uniform_key, help="Splits frames into equally partitioned frames")
    parser.add_argument('-n', '-N', '--N', type=int, required=True, default=1, help="Count for number of frames depending on method")
    parser.add_argument('-o', '-O', '--out', type=str, required=True, help="Directory to save the splits")
    return parser.parse_args()

def main():
    args = arg_parse()
    splitter(
        file_path=args.file,
        method=args.method,
        count=args.N,
        out_dir=args.out
    )

if __name__=='__main__':
    main()