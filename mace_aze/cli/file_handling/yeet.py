import argparse

from mace_aze.pipe.file_handling.frame2xyz import frame2xyz

def arg_parse():
    parser = argparse.ArgumentParser(description="Converts multiple coordinates file into single .xyz")
    parser.add_argument("-d","-D","--dir", type=str, required=True, help="Path to directory containing coordinate files")
    parser.add_argument('-n', '-N', '--N', type=int, default=-1, help="Number of frames to select. Chooses evenly")
    parser.add_argument("-o","-O", "--out", type=str, required=True, help="Path to storing the single xyz file")
    return parser.parse_args()

def main():
    args = arg_parse()
    frame2xyz(
        frames_dir=args.dir,
        out=args.out,
        count=args.N
    )

if __name__=='__main__':
    main()

