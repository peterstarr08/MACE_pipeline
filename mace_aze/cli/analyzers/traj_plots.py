import argparse
from mace_aze.analyzers import plot_models

def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--models-path', type=str, nargs='+', required=True, help="Space separated model paths")
    parser.add_argument('--traj-path', type=str, required=True, help="Path to trjectory file")
    parser.add_argument('--timestep', type=int, default=1, help="Time steps of of simualation")
    parser.add_argument('--interval', type=int, default=10, help="Time interval it was saved")
    parser.add_argument('--out', type=str, required=True, help="Output directory")
    return parser.parse_args()

def main():
    args = arg_parse()
    plot_models(traj_path=args.traj_path, time_unit=args.timestep, save_interval=args.interval, output_dir=args.out)


if __name__=="__main__":
    main()