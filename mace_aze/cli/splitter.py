import argparse
import os
from pathlib import Path
from ase.io import read, write
from ase import Atoms
from mace_aze.sampler import UniformSelector
from mace_aze.calculators import XTBCalculator
from mace_aze.utils.records import RawDataset, Dataset
from mace_aze.config import us_0_selected, us_off_selected
from mace_aze.log.conf import get_logger

log = get_logger(__name__)

#=================Args=======================
XTB_CALCULATOR_KEY = 'xtb'
#QM_CALCULATOR = "cp2k"

AUTO_SPLIT_RATIO = 0.9

calculator_keys=[XTB_CALCULATOR_KEY] #Add to this list if you add more calculators

AUTO_SPLIT = 'autoSplit'
TRAIN_KEY = 'trainKey'
TEST_KEY = 'testKey'

DEFAULT_VALUE_SPLIT = 'allSplit'


def arg_parser():
    parser = argparse.ArgumentParser(description="Generates energy and forces for each configuration. Atom groups were added before calacultions followed by training and test split.")
    parser.add_argument('--label', type=str, required=True, help="Label for the raw_data_pathset. If the label is benzene_cutoff_10, then program looks for raw_data_pathset/benzene/cutoff/10/benzene_10_cutoff__raw_dataset.xyz")
    
    #Right now default is xtb and only that is available
    parser.add_argument('--calculator', type=str, choices=calculator_keys, default=XTB_CALCULATOR_KEY, help="Method used to calculate forces and potential energies")

    parser.add_argument('--atoms', type=str, nargs='+', required=True, help="Atoms to calculate E0s. E.g. C H O")

    #Right now only sampler is Uniform Selector
    parser.add_argument('--uniform-selector', action='store_true', help="Flag for using uniform selector. Needs --offset [5]")
    parser.add_argument('--count', type=int, required=True, help="Number of configs to extract")
    parser.add_argument('--offset', type=int, default=5, help="Offset value for Uniform Selector")

    #Out label
    parser.add_argument('--out-label', type=str, required=True, help="Output label")

    return parser.parse_args()

def validate_arguments(label: str, atoms: list[str], us: bool, offset: int, count: int):
    log.info("Validating input")
    RawDataset.extract_path(label=label).exists() # Checks if the raw_dataset exists or not using the provided label
    if len(atoms) == 0: # Isolated Atoms cannot be 0
        raise ValueError("No atoms provided. Atoms are needed to calculate E0s")
    if us and offset<0: # With Uniform selector offset must be >=0
        raise ValueError("--offset cannot be less than 0 for Uniform Selector")
    if count <= 0: # Samples to be extracted cannot be less than 1
        raise ValueError("Require positive integer frames to extract")

def sample_config(db, count: int, us: bool, offset: int):
    '''
    One can chain sampling. For example, sample first using UniformSelector and then sample it using Farthest Point Sampling.
    
    key:
    Holds information whether any sampler was even use or not.
    If none of the sampler was used AUTO_SPLIT is true and every config will be considered for ab-intio calculations.
    The train and test split are done on default basis If any sampler was used, TRAIN_KEY and TEST_KEY holds split information for that sampler.

    *Right now only UniformSelector is used
    '''
    log.info("Sampling configuration")
    log.debug("Count: %d    UniformSelector: %s     offset:%d", count, str(us), offset)
    key = {
        AUTO_SPLIT: True,
        TRAIN_KEY: DEFAULT_VALUE_SPLIT,
        TEST_KEY: DEFAULT_VALUE_SPLIT
    }
    if us:
        UniformSelector(offset).select(db, count)
        key[AUTO_SPLIT] = False
        key[TRAIN_KEY] = us_0_selected
        key[TEST_KEY] = us_off_selected
    # Add more if cases for sampler and change the key to that sampler's sampling
    log.debug("Auto_split: %s   Train_key: %s   Test_key: %s", key[AUTO_SPLIT], key[TRAIN_KEY], key[TEST_KEY])
    return key

def calculate(db, key: dict, calculator: str, atoms: list[str]):
    selec_conf = []
    log.info("Extracting samples")
    if key[AUTO_SPLIT] is False: 
        selec_conf = [at for at in db if (key[TRAIN_KEY] in at.info or key[TEST_KEY] in at.info)]
    else:
        selec_conf = db
    log.info("Extraction completed")
    log.info("Adding isolated atoms: %s", ' '.join(atoms))
    isolatedAtom = [Atoms(symbol) for symbol in atoms]
    for at in isolatedAtom:
        at.info['config_type'] = 'IsolatedAtom'
        at.info[key[TRAIN_KEY]] = True # To include this in train set
    selec_conf = isolatedAtom + selec_conf

    log.info("Beginning calculations")
    if calculator==XTB_CALCULATOR_KEY:
        log.info("Using XTB calculator")
        XTBCalculator().calculate(selec_conf)
    
    return selec_conf

def write_configs(*db_lists: list[tuple[Path, list]]):
    for path, db in db_lists:
        path.parent.mkdir(parents = True)
        log.info("Writing to %s", str(path))
        write(path, db)


def save_config(label: str, db,  calc: str, key: dict):
    train_split = []
    test_split = []
    log.info("Splitting train and test set")
    if key[AUTO_SPLIT]:
        train_split = db[:int(len(db)*AUTO_SPLIT_RATIO)]
        test_split = db[int(len(db)*AUTO_SPLIT_RATIO):]
    else:
        for at in db:
            if key[TRAIN_KEY] in at.info:
                train_split.append(at)
            if key[TEST_KEY] in at.info:
                test_split.append(at)
    train_path = Dataset.extract_path(label=label+"_train", operation=calc)
    test_path = Dataset.extract_path(label=label+"_test", operation=calc)
    write_configs((train_path, train_split), (test_path, test_split))

def main():
    args = arg_parser() # Init arguments
    validate_arguments(label=args.label, atoms=args.atoms, us=args.uniform_selector, offset=args.offset, count=args.count) # Validate arguments
    log.info("Beginning splittor")
    #Reads configuration and generate sample keys. 'key' keeps track of usage of different sampler if used in chain. See the sampler_config() for more comments
    configs = read(RawDataset.extract_path(label=args.label), ':')
    key = sample_config(db=configs, count=args.count, us=args.uniform_selector, offset=args.offset)

    #Extracts the sampled config and calculats forces and energues for extracted configs only + for isolated atoms
    calculated_configs = calculate(db=configs, key=key, calculator=args.calculator, atoms=args.atoms)

    save_config(args.out_label, db=calculated_configs, calc=args.calculator, key=key)
    log.info("Splitter job's done!!!")


if __name__=="__main__":
    main()
    
