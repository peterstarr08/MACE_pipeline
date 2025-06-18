import argparse
import yaml
from pathlib import Path
from mace_aze.log.conf import get_logger
from mace_aze.pipe import (
    validate_yml,
    train_mace,
    mace_md,
    pipeline,
    generation,
    models_path,
    md_path,
    new_ds
)

log = get_logger(__name__)


def arg_parse():
    parser = argparse.ArgumentParser(description="Running a active MLP learning with MACE + OpenMM pipeline")
    parser.add_argument('--pipeline', type=str, required=True, help="Path to pipeline")
    return  parser.parse_args()

def file_exist(path: Path):
    if not path.exists():
        log.critical("%s file doesn't exist", str(path))
        raise FileNotFoundError("Incorrect file path")
    log.info("File found!")

def read_yaml(cfgPath: Path)->dict:
    log.info("Reading file %s", str(cfgPath))
    with open(cfgPath) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def run(cfg: dict):
    log.info("Back off! Running the pipeline")
    # Run training

    # Run MD

    # Read traj file

    # Committee calculations

    #Sample

    #DFT label

    #Write config

    #Repeat
    
    log.info("Pipline was succesfully executed!")

def main():
    args = arg_parse()
    path = Path(args.pipeline)
    
    file_exist(path)
    cfg = read_yaml(path)
    validate_yml(cfg)
    run(cfg)



if __name__ == "__main__":
    main()
