import argparse

from mace_aze.pipe.utils.coordinates_joiner import join

def arg_parse():
    parser = argparse.ArgumentParser("Combines multiple coordinates into single xyz frame")
    parser.add_argument("--path", type=str, nargs='+', required=True, help="Give a directory or list of paths to join")
    parser.add_argument("--out", type=str, required=True, help="Output path to single .xyz file")
    return parser.parse_args()

def main():
    args = arg_parse()
    join(
        paths=args.path,
        out=args.out
    )

if __name__=='__main__':
    main()