import argparse
import yaml
from pathlib import Path
from mace_aze.log.conf import get_logger
from mace_aze.pipe import (
    validate_yml,
    train_mace,
    mace_md,
    fix_atomic_energies_shape,
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


#===============Helper functions============================

def file_exist(path: Path):
    if not path.exists():
        log.critical("%s file doesn't exist", str(path))
        raise FileNotFoundError("Incorrect file path")
    log.info("Found %s", str(path))

def read_yaml(cfgPath: Path)->dict:
    log.info("Reading file %s", str(cfgPath))
    with open(cfgPath) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

#=================Training============================
def run_train():
    ...
def fix_model():
    ...

#==============MD openMM==============================
def run_openmm():
    ...
def extract_traj_path():
    ...

#==============Committee calculations===================
def run_committee_calc():
    ...

#===================Sampling========================
def run_sampling():
    ...
#=====================DFT labelling========================
def run_dft_labelling():
    ...

#==================Writing congs===========================
def write_train_set():
    ...


################Main Runner##############################

def run(cfg: dict):
    log.info("Back off! Running the pipeline")
    
    for i, gen in enumerate(cfg[pipeline]):
        if models_path in gen[f'{generation}{i}']:
            for mod_path in gen[f'{generation}{i}'][models_path]:
                #Chek exist
                #Do train
                #Fix model
                ...

        # Read traj file <--- Extracted from openmm config

        # Committee calculations <---Made

        #Sample <---Logic to be written here

        #DFT label <---Already implemented

        #Write config <--Easy

        #Repeat
        ...
    
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
