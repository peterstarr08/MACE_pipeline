import argparse
from mace_aze.pipe import fix_atomic_energies_shape
from mace_aze.log.conf import get_logger

log = get_logger(__name__)

def arg_parse():
    parser = argparse.ArgumentParser("Fixing atomic energies shape")
    parser.add_argument('--model-path', type=str, required=True, help="Path to model")
    return parser.parse_args()

def main():
    args = arg_parse()
    log.info("Beginning fixing MACE model at %s", arg_parse.model_path)
    fix_atomic_energies_shape(args.model_path)
    log.info("Done!!")

if __name__=="__main__":
    main()