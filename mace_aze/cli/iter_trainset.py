import argparse
from pathlib import Path 

from mace_aze.log.conf import get_logger
from mace_aze.calculators import XTBCalculator
from mace_aze.pipe import thershold_sample, top_disagreement_sample
from mace_aze.calculators.mace import mace_max_force_std

from ase.io import read, write

log = get_logger(__name__)

def arg_parse():
    parser = argparse.ArgumentParser("Generates training set for next iteration")
    parser.add_argument('--traj', type=str, required=True, help="Trajectory(.xyz) file path")
    parser.add_argument('--method', type=str, choices=['nikhilboi', 'top'], required=True, help="Method of sampling")
    parser.add_argument('--threshold', type=float, default=-1.0, help="Threshold for sampling. Required by 'nikhil")
    parser.add_argument('--count', type=int, default=-1, help="Number of samples to choose. Required  by 'top'")
    parser.add_argument('--prev-dataset', type=str, default=None, help="Add path to dataset you want to append to.")
    parser.add_argument('--calculator', type=str, choices=['xtb'], default='xtb', help="Calcaultor to evaluate the selected configurations")
    parser.add_argument('--out', type=str, required=True, help="Path to saving the .xyz file")
    return parser.parse_args()

def validate(meth: str, count: int, threshold: float):
    if meth=='nikhilboi':
        if threshold<=0:
            log.critical("'nikhilboi' requried positive floats")
            raise ValueError("Invald value provided")

    elif meth=='top':
        if count<=0:
            log.critical("'top' requires positive sample to selct from")
            raise ValueError("Invalid value provided")
def main():
    args = arg_parse()
    validate(meth=args.method, count=args.count, threshold=args.threshold)
    log.debug("Arguments validated")

    traj = read(args.traj, ':')
    dataset = []
    if args.prev_dataset is not None:
        log.info("Previous dataset provided. Reading %s", args.prev_dataset)
        dataset = read(args.prev_dataset, ':')
        log.info("Successfully read %d configs", len(dataset))

    log.info("Sampling method: %s", args.method)
    if args.method=='nikhilboi':
        traj = thershold_sample(configs=traj, threshold=args.threshold, key=mace_max_force_std)
    elif args.method=='top':
        traj = top_disagreement_sample(configs=traj, count=args.count, key=mace_max_force_std)
    else:
        log.warning("No sampling method provided. This is unexpected")
    
    log.info("Calcaultor: %s", args.calculator)
    if args.calculator=='xtb':
        XTBCalculator().calculate(traj)

    dataset = dataset + traj
    log.info("Total dataset size: %d", len(dataset))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    log.info("Writing to %s", str(out_path))
    write(out_path, dataset)
    log.info("Done!")


if __name__=="__main__":
    main()