import argparse

from mace_aze.analyzers import plot_models, plot_pes


def trajactory_plotter(args):
    plot_models(
        traj_path=args.traj_path,
        save_interval=args.interval,
        output_dir=args.out
    )

def pes_plotter(args): # Potential Energy Surface
    plot_pes(
        xyz_path=args.file,
        energy_key=args.energy_key,
        out_path=args.out
    )

def arg_parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="plt_type")

    traj_parser = subparsers.add_parser('trajectory', description="Plots trajectory analysis for next active learning iterations")
    traj_parser.add_argument('--traj-path', type=str, required=True, help="Path to trjectory file")
    traj_parser.add_argument('--interval', type=int, default=10, help="Time interval between framesm were saved")
    traj_parser.add_argument('--out', type=str, required=True, help="Output directory")    
    traj_parser.set_defaults(func=trajactory_plotter)

    pes_parser = subparsers.add_parser('pes', description="Potential energy for each frames")
    pes_parser.add_argument('-f', '-F', '--file', type=str, required=True, help="Path to .xyz labelled data")
    pes_parser.add_argument('-e', '-E', '--energy-key', type=str, required=True, help="Energy key to look for")
    pes_parser.add_argument('-o', '-O', '--out', type=str, required=True, help="Plot output path")    
    pes_parser.set_defaults(func=pes_plotter)

    return parser.parse_args()

def main():
    args = arg_parse()
    args.func(args)

if __name__=='__main__':
    main()