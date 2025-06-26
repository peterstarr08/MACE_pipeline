import argparse

from mace_aze.config import (
    split_methods,
    uniform_key
)
from mace_aze.pipe.file_handling.frame2xyz import frame2xyz
from mace_aze.pipe.file_handling.splitter import splitter

def split_func(args):
    splitter(
        file_path=args.file,
        method=args.method,
        count=args.N,
        out_dir=args.out
    )

def yeet_func(args):
    frame2xyz(
        frames_dir=args.dir,
        out=args.out,
        count=args.N
    )


def arg_parse():
    parser = argparse.ArgumentParser("Calculating DFT")
    subparsers = parser.add_subparsers(dest="handler")

    splitArgs = subparsers.add_parser('split', description="Splits single config file to muliple based on selection method")
    splitArgs.add_argument('-f','-F','--file', type=str, required=True, help="Input file")
    splitArgs.add_argument('-m', '-M', '--method', type=str, choices=split_methods, default=uniform_key, help="Splits frames into equally partitioned frames")
    splitArgs.add_argument('-n', '-N', '--N', type=int, required=True, default=1, help="Count for number of frames depending on method")
    splitArgs.add_argument('-o', '-O', '--out', type=str, required=True, help="Directory to save the splits")
    splitArgs.set_defaults(func=split_func)


    yeetArgs = subparsers.add_parser('yeet', description="Converts multiple coordinates file into single .xyz")
    yeetArgs.add_argument("-d","-D","--dir", type=str, required=True, help="Path to directory containing coordinate files")
    yeetArgs.add_argument('-n', '-N', '--N', type=int, default=-1, help="Number of frames to select. Chooses evenly")
    yeetArgs.add_argument("-o","-O", "--out", type=str, required=True, help="Path to storing the single xyz file")
    yeetArgs.set_defaults(func=yeet_func)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=='__main__':
    main()