import argparse
from mace_aze.pipe import comm_eval

def arg_parse():
    parser = argparse.ArgumentParser("To evaluate a committe from a .pdb OpenMM trjajectory")
    parser.add_argument('--models-path', type=str, nargs='+', required=True, help="Space separated model paths")
    parser.add_argument('--traj-path', type=str, required=True, help="Path to trjectory file. Will you this directory to find mace_md.log for temperatures")
    return parser.parse_args()

def main():
    args = arg_parse()
    comm_eval(model_paths=args.models_path, traj_path=args.traj_path)


if __name__=="__main__":
    main()