import argparse
from mace_aze.analyzers import plot_models

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--models-path', type=str, nargs='+', required=True, help="Space separated model paths")
    parser.add_argument('--traj-path', type=str, required=True, help="Path to trjectory file. Will you this directory to find mace_md.log for temperatures")
    parser.add_argument('--timestep', type=int, default=1, help="Time steps for simulation for plotting X axes")
    parser.add_argument('--out', type=str, required=True, help="Output directory")
    return parser.parse_args()

def main():
    args = arg_parse()
    plot_models(traj_path=args.traj_path, model_paths=args.models_path, time_unit=args.timestep, output_dir=args.out)


if __name__=="__main__":
    main()