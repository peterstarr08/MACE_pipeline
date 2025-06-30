import argparse

from mace_aze.pipe.sampling.fps_sampling import fps_select


def fps_interface(args):
    fps_select(
        configs_path=args.file,
        count=args.count,
        out_path=args.out
    )

def arg_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="sample_meth")

    fps_parser = subparsers.add_parser('fps', description="Farthest Point Sampling")
    fps_parser.add_argument('-f', '-F', '--file', type=str, required=True, help="Path to condifs files")
    fps_parser.add_argument('-n','-N', '--count', type=int, required=True, help="Number of frames to choose")
    fps_parser.add_argument('-o','-O','--out', type=str, default=None, help="Path to store the sampled configs. Otherwise will be stored in same directory of source")
    fps_parser.set_defaults(func=fps_interface)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=='__main__':
    main()