import argparse

from mace_aze.pipe.gaussian.log_to_xyz import log_to_xyz

def arg_parse():
    parser = argparse.ArgumentParser(description="Converts all gaussian output files to single .xyz files with forces and energy labelled")
    parser.add_argument('--dir', type=str, required=True, help="Path to directory which contains .log files")
    parser.add_argument('--out', type=str, required=True, help="Path to save the xyz file")
    return parser.parse_args()

def main():
    args = arg_parse()
    log_to_xyz(
        log_dir=args.dir,
        xyz_file=args.out
    )

if __name__=="__main__":
    main()