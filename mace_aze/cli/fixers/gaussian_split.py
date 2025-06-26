import argparse

from mace_aze.pipe.gaussian.xyz_to_com import xyz_to_com

method_choice = ['B3LYP']
method_basis = ['6-31G(d)']

def arg_parse():
    parser = argparse.ArgumentParser(description="Splits a .xyz trajectory to many gaussian input files for calculating energy and forces on each atom")
    parser.add_argument('--traj', type=str, required=True, help="Path to trajectory")
    parser.add_argument('--method', type=str, choices=method_choice, default=method_choice[0], help="DFT method for Gaussian")
    parser.add_argument('--basis', type=str, choices=method_basis, default=method_basis[0], help="DFT basis set")
    parser.add_argument('--dir', type=str, required=True, help="Output directory.\n Warning: It overwrites any exiisitng files")
    return parser.parse_args()

def main():
    args = arg_parse()
    xyz_to_com(
        xyz_file=args.traj,
        output_dir=args.dir,
        method=args.method,
        basis=args.basis
    )

if __name__=='__main__':
    main()