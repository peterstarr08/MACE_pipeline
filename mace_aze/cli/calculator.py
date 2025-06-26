import argparse

from mace_aze.config import(
    xtb_key
)
from mace_aze.pipe.calculators.xtb import xtb_calculator

def xtb_calculate(args):
    xtb_calculator(
        path=args.path,
        atoms=args.atoms,
        split_ratio=args.split,
        keep_isoatoms=args.keep_isoatoms
    )
    

def arg_parse():
    parser = argparse.ArgumentParser("Calculating DFT")
    subparsers = parser.add_subparsers(dest="calc")

    xtbCalc = subparsers.add_parser(xtb_key)
    xtbCalc.add_argument('-p','-P','--path', type=str, required=True, help="Path to coordinate file to calculate their XTB energgy and forces")
    xtbCalc.add_argument('--atoms', type=str, nargs='+', required=True, help="Atoms for Isolate Atom Energies")
    xtbCalc.add_argument('--split', type=float, default=0.5, help="Split ratio for train and test")
    xtbCalc.add_argument('--keep-isoatoms', action='store_true', help="Whether to keep isolated atoms")
    xtbCalc.set_defaults(func=xtb_calculate)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=="__main__":
    main()