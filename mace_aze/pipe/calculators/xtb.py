import numpy as np
from pathlib import Path

from mace_aze.calculators import XTBCalculator
from mace_aze.log.conf import get_logger

from ase import Atoms
from ase.io import read, write

log = get_logger(__name__)

def split_db(db, ratio):
    total = len(db)
    n_train = int(total * (1 - ratio))
    
    train_indices = np.linspace(0, total - 1, n_train, dtype=int)
    train_set = [db[i] for i in train_indices]

    all_indices = set(range(total))
    test_indices = sorted(all_indices - set(train_indices))
    test_set = [db[i] for i in test_indices]

    log.debug("Train Indices: %s", str(train_indices))
    log.debug("Test Indices: %s", str(test_indices))

    return train_set, test_set

def xtb_calculator(path: str, atoms: list[str], split_ratio: float, keep_isoatoms: bool=True):
    path = Path(path).resolve(strict=True)

    log.info("Atoms: %s     Split Ratio: %f     Keep Isolated Atoms: %s", str(atoms), split_ratio, str(keep_isoatoms))

    log.info("Reading %s", str(path))
    db = read(path, ':')
    log.info("Read %d configs", len(db))
    
 
    isolated_atoms = [Atoms(sym) for sym in atoms]
    for at in isolated_atoms:
        at.info['config_type'] = 'IsolatedAtom'
    log.debug("Adding %d isolated atoms", len(isolated_atoms))
    db = isolated_atoms + db

    log.info("Starting XTB calculation")
    XTBCalculator().calculate(db)
    log.info("XTB calculations done")

    isolated_atoms = db[:len(isolated_atoms)]
    db = db[len(isolated_atoms):]

    train_db, test_db = split_db(db, split_ratio)

    if keep_isoatoms:
        log.debug("Adding isolated atoms back to db")
        train_db = isolated_atoms + train_db
    
    file_name = path.stem
    train_path = path.with_name(file_name + "__xtb_train.xyz")
    test_path = path.with_name(file_name + "__xtb_test.xyz")

    log.info("Writing %s", str(train_path))
    write(train_path, train_db)
    log.info("Writing %s", str(test_path))
    write(test_path, test_db)

    log.info("Done !!!")


    
