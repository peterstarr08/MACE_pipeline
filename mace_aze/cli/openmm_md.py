import argparse
from mace_aze.pipe import mace_md

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help="Path to OpenMM configs")
    return parser.parse_args()


def main():
    args = arg_parse()
    mace_md(args.config)

if __name__=='__main__':
    main()